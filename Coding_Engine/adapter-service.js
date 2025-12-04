/**
 * Azure Session Pool Adapter Service
 * Listens on Azure-provided port, handles Azure API, translates to Piston API
 */

const http = require('http');
const url = require('url');

// Use Azure-provided port if present, else default 2000
const PORT = process.env.CONTAINER_APP_PORT || process.env.INGRESS_PORT || process.env.PORT || 2000;
const LISTEN_PORT = parseInt(PORT, 10);

const PISTON_PORT = 2001; // Piston runs on port 2001 (via socat forwarding)

const LANGUAGE_MAP = {
    'python': 'python',
    'cpp': 'c++',
    'c++': 'c++',
    'java': 'java',
    'javascript': 'javascript',
    'js': 'javascript'
};

const VERSION_MAP = {
    'python': '3.10.0',
    'c++': '10.2.0',
    'cpp': '10.2.0',
    'java': '15.0.2',
    'javascript': '16.3.0',
    'js': '16.3.0'
};

const EXTENSION_MAP = {
    'python': 'py',
    'cpp': 'cpp',
    'c++': 'cpp',
    'java': 'java',
    'javascript': 'js',
    'js': 'js'
};

function translateToPiston(azurePayload, language, version) {
    const props = azurePayload.properties || {};
    const code = props.code || '';
    const stdin = props.stdin || '';
    
    const ext = EXTENSION_MAP[language] || 'txt';
    const filename = `main.${ext}`;
    
    return {
        language: LANGUAGE_MAP[language] || language,
        version: version || VERSION_MAP[language] || 'latest',
        files: [{
            name: filename,
            content: code
        }],
        stdin: stdin,
        args: [],
        compile_timeout: 10000,
        run_timeout: 3000,
        compile_memory_limit: -1,
        run_memory_limit: -1
    };
}

function translateToAzure(pistonResponse) {
    const run = pistonResponse.run || {};
    
    return {
        properties: {
            status: run.code === 0 ? 'Success' : 'Failed',
            stdout: run.stdout || '',
            stderr: run.stderr || '',
            exitCode: run.code || 1
        }
    };
}

function callPiston(pistonPayload) {
    return new Promise((resolve, reject) => {
        const postData = JSON.stringify(pistonPayload);
        
        const options = {
            hostname: 'localhost',
            port: PISTON_PORT,
            path: '/api/v2/execute',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData)
            },
            timeout: 30000
        };
        
        const req = http.request(options, (res) => {
            let data = '';
            
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                if (!data || data.trim() === '') {
                    reject(new Error('Empty response from Piston'));
                    return;
                }
                try {
                    const jsonData = JSON.parse(data);
                    if (res.statusCode === 200) {
                        resolve(jsonData);
                    } else {
                        reject(new Error(`Piston API error: ${res.statusCode} - ${data}`));
                    }
                } catch (e) {
                    reject(new Error(`Failed to parse Piston response: ${e.message}. Data: ${data.substring(0, 200)}`));
                }
            });
        });
        
        req.on('error', (e) => {
            reject(new Error(`Request to Piston failed: ${e.message}`));
        });
        
        req.on('timeout', () => {
            req.destroy();
            reject(new Error('Request to Piston timed out'));
        });
        
        req.write(postData);
        req.end();
    });
}

async function handleExecute(req, res, language) {
    let body = '';
    
    req.on('data', (chunk) => {
        body += chunk.toString();
    });
    
    req.on('end', async () => {
        try {
            const azurePayload = JSON.parse(body);
            const queryParams = url.parse(req.url, true).query;
            const version = queryParams.version || VERSION_MAP[language];
            
            console.log(`[EXECUTE] Language: ${language}, Version: ${version}`);
            
            const pistonPayload = translateToPiston(azurePayload, language, version);
            const pistonResponse = await callPiston(pistonPayload);
            const azureResponse = translateToAzure(pistonResponse);
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(azureResponse));
            
        } catch (error) {
            console.error('[EXECUTE ERROR]', error);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({
                error: {
                    code: 'InternalServerError',
                    message: error.message
                }
            }));
        }
    });
}

function handleHealthCheck(req, res) {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('ok');
}

function handleReadyCheck(req, res) {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('ready');
}

const server = http.createServer((req, res) => {
    // Log every request (critical for debugging)
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;
    console.log(`[${new Date().toISOString()}] ${req.method} ${pathname} - Query: ${JSON.stringify(parsedUrl.query)}`);
    console.log(`[REQUEST] Full URL: ${req.url}`);
    console.log(`[REQUEST] Headers: ${JSON.stringify(req.headers)}`);
    
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // Health endpoints (must be fast & return 200)
    if (pathname === '/health') {
        handleHealthCheck(req, res);
        return;
    }
    
    if (pathname === '/ready') {
        handleReadyCheck(req, res);
        return;
    }
    
    // Root endpoint
    if (pathname === '/') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ 
            status: 'running', 
            service: 'Azure Session Pool Adapter',
            port: LISTEN_PORT,
            pistonPort: PISTON_PORT
        }));
        return;
    }
    
    // Match /{language}/execute (e.g., /python/execute, /cpp/execute)
    const executeMatch = pathname.match(/^\/(\w+)\/execute$/);
    if (executeMatch && req.method === 'POST') {
        const language = executeMatch[1].toLowerCase();
        if (LANGUAGE_MAP[language] || language in VERSION_MAP) {
            handleExecute(req, res, language);
            return;
        }
    }
    
    // 404 for unknown endpoints
    console.log(`[404] Path not matched: ${pathname}`);
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ 
        message: 'Not Found', 
        path: pathname,
        supportedLanguages: Object.keys(LANGUAGE_MAP)
    }));
});

// CRITICAL: Bind to 0.0.0.0 so Azure can reach it
server.listen(LISTEN_PORT, '0.0.0.0', () => {
    console.log(`========================================`);
    console.log(`Azure Session Pool Adapter`);
    console.log(`Listening on 0.0.0.0:${LISTEN_PORT}`);
    console.log(`Piston API on localhost:${PISTON_PORT}`);
    console.log(`CONTAINER_APP_PORT: ${process.env.CONTAINER_APP_PORT || 'not set'}`);
    console.log(`PORT: ${process.env.PORT || 'not set'}`);
    console.log(`========================================`);
});

server.on('error', (err) => {
    console.error('Server error:', err);
    process.exit(1);
});

process.on('SIGTERM', () => {
    console.log('SIGTERM received, shutting down gracefully');
    server.close(() => {
        console.log('Server closed');
        process.exit(0);
    });
});


