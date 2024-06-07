document.addEventListener('DOMContentLoaded', function() {
    const addAppForm = document.getElementById('add-app-form');
    
    addAppForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(addAppForm);
        fetch('/api/apps/', {
            method: 'POST',
            body: formData,
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        }).then(response => response.json())
        .then(data => {
            if (data.id) {
                alert('App added successfully');
                addAppForm.reset();
            } else {
                alert('Failed to add app');
            }
        });
    });

    const dropArea = document.getElementById('drop-area');

    dropArea.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropArea.classList.add('drag-over');
    });

    dropArea.addEventListener('dragleave', () => {
        dropArea.classList.remove('drag-over');
    });

    dropArea.addEventListener('drop', (event) => {
        event.preventDefault();
        dropArea.classList.remove('drag-over');

        const files = event.dataTransfer.files;
        handleFiles(files);
    });

    function handleFiles(files) {
        const formData = new FormData();
        formData.append('screenshot', files[0]);
        formData.append('app', dropArea.getAttribute('data-app-id'));

        fetch('/api/tasks/', {
            method: 'POST',
            body: formData,
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        }).then(response => response.json())
        .then(data => {
            if (data.id) {
                alert('Screenshot uploaded successfully');
            } else {
                alert('Failed to upload screenshot');
            }
        });
    }
});

function startTask(appId) {
    const dropArea = document.getElementById('drop-area');
    dropArea.setAttribute('data-app-id', appId);
    dropArea.style.display = 'block';
}
