document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const resultsSection = document.getElementById('results-section');
    const tableBody = document.getElementById('results-table-body');
    const loader = document.getElementById('loader');
    const sortSelect = document.getElementById('sort-select');
    const filterStatus = document.getElementById('filter-status');

    let allResults = [];

    // Initial Load from History
    fetchHistory();

    async function fetchHistory() {
        try {
            const response = await fetch('/history');
            if (response.ok) {
                allResults = await response.json();
                if (allResults.length > 0) {
                    applySorting();
                    resultsSection.classList.remove('hidden');
                }
            }
        } catch (e) { console.error("History load error", e); }
    }

    // Drag and Drop handlers
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        handleFiles(e.dataTransfer.files);
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    sortSelect.addEventListener('change', () => {
        applySorting();
    });

    filterStatus.addEventListener('change', () => {
        applySorting();
    });

    function parseDate(dateStr) {
        if (!dateStr || dateStr === 'N/A') return new Date(8640000000000000); // Far future
        const d = new Date(dateStr);
        return isNaN(d) ? new Date(8640000000000000) : d;
    }

    function applySorting() {
        const sortVal = sortSelect.value;
        const filterVal = filterStatus.value;
        
        let processedData = [...allResults];

        // Apply Filter
        if (filterVal === 'finished') {
            processedData = processedData.filter(item => item.finished);
        } else if (filterVal === 'pending') {
            processedData = processedData.filter(item => !item.finished);
        }

        // Apply Sort
        if (sortVal === 'upload_time_desc') {
            processedData.sort((a, b) => new Date(b.upload_time) - new Date(a.upload_time));
        } else if (sortVal === 'upload_time_asc') {
            processedData.sort((a, b) => new Date(a.upload_time) - new Date(b.upload_time));
        } else if (sortVal === 'deadline_asc') {
            processedData.sort((a, b) => parseDate(a.deadline) - parseDate(b.deadline));
        } else if (sortVal === 'deadline_desc') {
            processedData.sort((a, b) => parseDate(b.deadline) - parseDate(a.deadline));
        }

        renderTable(processedData);
    }

    async function handleFiles(files) {
        if (files.length === 0) return;

        loader.classList.remove('hidden');
        resultsSection.classList.add('hidden');
        
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }

        try {
            const response = await fetch('/parse', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Upload failed');
            }

            const results = await response.json();
            allResults = results;
            applySorting();
            
            loader.classList.add('hidden');
            resultsSection.classList.remove('hidden');
        } catch (error) {
            console.error(error);
            alert(`Error: ${error.message}\n\nPlease check if the file is open in another program and ensure the 'storage' folder is writable.`);
            loader.classList.add('hidden');
        }
    }

    function renderTable(data) {
        tableBody.innerHTML = '';
        data.forEach(item => {
            const row = document.createElement('tr');
            row.className = `border-b hover:bg-gray-50 transition-colors ${item.finished ? 'bg-gray-50 text-gray-400' : ''}`;
            
            const fileLink = item.saved_filename ? `/files/${item.saved_filename}` : '#';
            const uid = item.saved_filename; // Use the unique physical filename as ID

            row.innerHTML = `
                <td class="p-4 text-sm truncate max-w-xs" title="${item.filename}">
                    <a href="${fileLink}" target="_blank" class="text-blue-600 hover:underline flex items-center gap-2">
                        <i class="far fa-file-alt"></i> ${item.filename}
                    </a>
                </td>
                <td class="p-4 text-sm font-medium ${item.finished ? 'line-through' : 'text-gray-900'}">${item.job_title}</td>
                <td class="p-4 text-sm">${item.id || 'N/A'}</td>
                <td class="p-4 text-sm">${item.deadline || 'N/A'}</td>
                <td class="p-4 text-sm">${item.duty_station || 'N/A'}</td>
                <td class="p-4 text-center">
                    <input type="checkbox" 
                           ${item.finished ? 'checked' : ''} 
                           onchange="toggleStatus('${uid}')"
                           class="w-5 h-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500 cursor-pointer">
                </td>
                <td class="p-4 text-center">
                    <button onclick="deleteJob('${uid}')" class="text-red-500 hover:text-red-700 transition-colors" title="Delete">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    }

    window.toggleStatus = async function(uid) {
        try {
            const response = await fetch(`/toggle-finished/${uid}`, { method: 'POST' });
            if (response.ok) {
                const res = await response.json();
                // Update local data
                allResults = allResults.map(item => {
                    if (item.saved_filename === uid) {
                        return { ...item, finished: res.finished };
                    }
                    return item;
                });
                applySorting();
            }
        } catch (e) {
            console.error("Toggle error", e);
        }
    };

    window.deleteJob = async function(uid) {
        if (!confirm("Are you sure you want to delete this JD and its saved file?")) return;
        
        try {
            const response = await fetch(`/delete/${uid}`, { method: 'POST' });
            if (response.ok) {
                // Update local data
                allResults = allResults.filter(item => item.saved_filename !== uid);
                applySorting();
                if (allResults.length === 0) {
                    resultsSection.classList.add('hidden');
                }
            }
        } catch (e) {
            console.error("Delete error", e);
        }
    };

    window.exportToCSV = function() {
        if (allResults.length === 0) return;

        const headers = ["Filename", "Job Title", "ID", "Deadline", "Duty Station", "Finished"];
        const csvContent = [
            headers.join(","),
            ...allResults.map(r => [
                `"${r.filename}"`,
                `"${r.job_title}"`,
                `"${r.id}"`,
                `"${r.deadline}"`,
                `"${r.duty_station}"`,
                `"${r.finished ? 'Yes' : 'No'}"`
            ].join(","))
        ].join("\n");

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement("a");
        const url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", `UN_JD_Analysis_${new Date().toISOString().split('T')[0]}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };
});
