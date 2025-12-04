function solve() {
    // Your code here for Longest Substring Without Repeating Characters
    return 0;
}

const readline = require('readline');
const rl = readline.createInterface({input: process.stdin, output: process.stdout});
rl.on('line', (line) => {
    const n = parseInt(line);
    console.log(solve());
    rl.close();
});
