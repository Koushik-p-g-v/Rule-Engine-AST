function fetchRuleString(dropdownId, inputId) {
    document.getElementById(dropdownId).addEventListener('change', function() {
        const selectedRuleName = this.value;
        if (selectedRuleName) {
            fetch(`/get_rule_string?name=${encodeURIComponent(selectedRuleName)}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById(inputId).value = data.rule_string;
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        } else {
            document.getElementById(inputId).value = '';
        }
    });
}

// Apply the function for both dropdowns
fetchRuleString('rule-name-evaluate', 'rule-to-evaluate');
fetchRuleString('rule-name-modify', 'rule-to-modify');


// Handle adding a rule
document.getElementById('createRuleModal').addEventListener('submit', function(event) {
    event.preventDefault();
    const rule = document.getElementById('rule').value;

    fetch('/add_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule: rule }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('rule').value = ''; // Clear the input
        $('#createRuleModal').modal('hide'); // Hide the modal
        showResultModal(data.message); // Show result
        fetchAndUpdateRules(); // Refresh rules
    })
    .catch(error => console.error('Error adding rule:', error));
});

// Handle evaluating a rule
document.getElementById('evaluateRuleModal').addEventListener('submit', function(event) {
    event.preventDefault();
    const rule = document.getElementById('rule-to-evaluate').value;
    const ruleName = document.getElementById('rule-name-evaluate').value;
    const data = document.getElementById('data').value;

    fetch('/evaluate_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule: rule, rule_name: ruleName, data: JSON.parse(data) }),
    })
    .then(response => response.json())
    .then(data => {
        $('#evaluateRuleModal').modal('hide'); // Hide the modal
        showResultModal(data.result); // Show result
    })
    .catch(error => console.error('Error evaluating rule:', error));
});

// Handle combining rules
document.getElementById('combineRuleModal').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const rules = document.getElementById('combrules').value.trim().split('\n');
    const selectedRuleNames = Array.from(document.getElementById('rule-names-combine').selectedOptions).map(option => option.value);

    fetch('/combine_rule', {
        method: 'POST', // Ensure this matches the Flask route method
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rules: rules, rule_names: selectedRuleNames }),
    })
    .then(response => {
        // Check if the response status is OK (200) or not
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error || 'Something went wrong'); });
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('combrules').value = ''; // Clear the input
        $('#combineRuleModal').modal('hide'); // Hide the modal
        showResultModal(data.message); // Show result
        fetchAndUpdateRules(); // Refresh rules
    })
    .catch(error => {
        console.error('Error combining rules:', error);
        alert(error.message); // Display error message
    });
});


// Handle deleting rules
document.getElementById('deleteRuleModal').addEventListener('submit', function(event) {
    event.preventDefault();
    const selectedRules = Array.from(document.getElementById('rule-name-delete').selectedOptions).map(option => option.value);

    fetch('/delete_rule', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rules: selectedRules }),
    })
    .then(response => response.json())
    .then(data => {
        $('#deleteRuleModal').modal('hide'); // Hide the modal
        showResultModal(data.result); // Show result
        fetchAndUpdateRules(); // Refresh rules
    })
    .catch(error => console.error('Error deleting rules:', error));
});

// Handle modifying a rule
document.getElementById('modifyRuleModal').addEventListener('submit', function(event) {
    event.preventDefault();
    const ruleName = document.getElementById('rule-name-modify').value;
    const modifiedRule = document.getElementById('rule-to-modify').value;

    fetch('/modify_rule', {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule_name: ruleName, rule: modifiedRule }),
    })
    .then(response => response.json())
    .then(data => {
        $('#modifyRuleModal').modal('hide'); // Hide the modal
        showResultModal(data.result); // Show result
        fetchAndUpdateRules(); // Refresh rules
    })
    .catch(error => console.error('Error modifying rule:', error));
});

// Function to refresh rules
function fetchAndUpdateRules() {
    
    fetch('/get_rule_data')
    .then(response => response.json())
    .then(data => {
        const rulesTableBody = document.querySelector('#rulesTable tbody');
        rulesTableBody.innerHTML = '';
        data.forEach(rule => {
            const row = document.createElement('tr');
            const nameCell = document.createElement('td');
            nameCell.textContent = rule.name;
            row.appendChild(nameCell);
            const ruleStringCell = document.createElement('td');
            ruleStringCell.textContent = rule.rule_string;
            row.appendChild(ruleStringCell);
            rulesTableBody.appendChild(row);
        });
    })
    .catch(error => console.error('Error fetching rule data:', error));
}

        // Fetch rule names from the server and populate the dropdowns
        fetch('/get_rule_names')
            .then(response => response.json())
            .then(data => {
                const evaluateDropdown = document.getElementById('rule-name-evaluate');
                const combineDropdown = document.getElementById('rule-names-combine');
                const deleteDropdown = document.getElementById('rule-name-delete');
                const modifyDropdown = document.getElementById('rule-name-modify');

                data.forEach(ruleName => {
                    const option = document.createElement('option');
                    option.value = ruleName;
                    option.textContent = ruleName;
                    evaluateDropdown.appendChild(option);

                    const optionClone1 = option.cloneNode(true);
                    const optionClone2 = option.cloneNode(true);
                    const optionClone3 = option.cloneNode(true);
                    combineDropdown.appendChild(optionClone1);
                    deleteDropdown.appendChild(optionClone2);
                    modifyDropdown.appendChild(optionClone3);
                });
            });

// Function to show result in modal
function showResultModal(message) {
    document.getElementById('resultMessage').innerText = message;
    $('#resultModal').modal('show'); // Show the result modal
}

document.getElementById('reload').addEventListener('click', function() {
            location.reload();  // Reload the webpage when "OK" button is clicked
});

fetchAndUpdateRules();