document.getElementById('run-script-btn').addEventListener('click', async () => {
    const outputDiv = document.getElementById('output');
    outputDiv.textContent = 'Running script...';

    try {
        const response = await fetch('/run-script', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const data = await response.json();
        outputDiv.textContent = `Output: ${data.output}\nExecution Time: ${data.executionTime} ms`;
    } catch (error) {
        outputDiv.textContent = `Error: ${error.message}`;
    }
});