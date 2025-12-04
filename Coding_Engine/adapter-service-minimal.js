/**
 * MINIMAL Adapter - Just to test if Azure forwards requests
 * Returns mock responses to verify the flow works
 */

const http = require('http');

// Use Azure-provided port or default 2000
const PORT = process.env.CONTAINER_APP_PORT || process.env.INGRESS_PORT || process.env.PORT || 2000;
const LISTEN_PORT = parseInt(PORT, 10);

const server = http.createServer((req, res) => {
    const url = require('url');
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;
    
    // Log EVERYTHING to see what Azure sends
    console.log(`\n========== REQUEST RECEIVED ==========`);
    console.log(`Time: ${new Date().toISOString()}`);
    console.log(`Method: ${req.method}`);
    console.log(`Full URL: ${req.url}`);
    console.log(`Pathname: ${pathname}`);
    console.log(`Query: ${JSON.stringify(parsedUrl.query)}`);
    console.log(`Headers: ${JSON.stringify(req.headers)}`);
    console.log(`=======================================\n`);
    
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // Health endpoints (Azure probes these)
    if (pathname === '/health' || pathname === '/ready') {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('ok');
        return;
    }
    
    // Root endpoint
    if (pathname === '/') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ 
            status: 'running', 
            service: 'Minimal Test Adapter',
            port: LISTEN_PORT,
            message: 'This is a test container to verify Azure forwarding'
        }));
        return;
    }
    
    // Handle /python/execute (or any /{language}/execute)
    const executeMatch = pathname.match(/^\/(\w+)\/execute$/);
    if (executeMatch && req.method === 'POST') {
        const language = executeMatch[1].toLowerCase();
        
        let body = '';
        req.on('data', (chunk) => {
            body += chunk.toString();
        });
        
        req.on('end', () => {
            console.log(`[EXECUTE] Language: ${language}`);
            console.log(`[EXECUTE] Body: ${body.substring(0, 200)}`);
            
            // Return MOCK response (Azure format)
            const mockResponse = {
                properties: {
                    status: 'Success',
                    stdout: `Mock execution for ${language}\nThis proves Azure forwarded the request!`,
                    stderr: '',
                    exitCode: 0
                }
            };
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(mockResponse));
        });
        return;
    }
    
    // 404 for unknown endpoints
    console.log(`[404] Path not matched: ${pathname}`);
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ 
        message: 'Not Found', 
        path: pathname,
        receivedUrl: req.url,
        supportedEndpoints: ['/health', '/ready', '/python/execute', '/cpp/execute', '/java/execute', '/javascript/execute']
    }));
});

// CRITICAL: Bind to 0.0.0.0 so Azure can reach it
server.listen(LISTEN_PORT, '0.0.0.0', () => {
    console.log(`========================================`);
    console.log(`MINIMAL TEST ADAPTER`);
    console.log(`Listening on 0.0.0.0:${LISTEN_PORT}`);
    console.log(`CONTAINER_APP_PORT: ${process.env.CONTAINER_APP_PORT || 'not set'}`);
    console.log(`PORT: ${process.env.PORT || 'not set'}`);
    console.log(`========================================`);
    console.log(`This container returns MOCK responses`);
    console.log(`to verify Azure forwards requests correctly`);
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

