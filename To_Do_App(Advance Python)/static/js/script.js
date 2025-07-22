document.addEventListener('DOMContentLoaded', () => {
    const todoForm = document.getElementById('todo-form');
    const taskInput = document.getElementById('task-input');

    if (todoForm && taskInput) {
        taskInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                todoForm.submit();
            }
        });

        taskInput.focus();

        todoForm.addEventListener('submit', () => {
            setTimeout(() => taskInput.value = '', 100);
        });
    }

    document.querySelectorAll('.complete-btn, .undo-btn').forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            const todoId = e.target.getAttribute('data-id');
            const todoItem = e.target.closest('.todo-item');
            
            e.target.disabled = true;
            e.target.textContent = 'Loading...';
            
            try {
                const response = await fetch(`/complete/${todoId}`, { method: 'GET' });
                if (response.ok) {
                    const isCompleting = e.target.classList.contains('complete-btn');
                    showCustomAlert(isCompleting ? 'Task completed!' : 'Task marked as incomplete', 'success');
                    
                    todoItem.style.opacity = '0.5';
                    setTimeout(() => location.reload(), 800);
                } else {
                    throw new Error('Failed to update');
                }
            } catch (error) {
                console.error('Error:', error);
                showCustomAlert('Failed to update task', 'error');
                e.target.disabled = false;
                e.target.textContent = e.target.classList.contains('complete-btn') ? 'Complete' : 'Undo';
            }
        });
    });

    const modal = document.getElementById('confirmModal');
    const modalCancel = document.getElementById('modalCancel');
    const modalConfirm = document.getElementById('modalConfirm');
    let pendingDeleteAction = null;

    function showModal() {
        modal.style.display = 'flex';
        modal.classList.add('show');
        modalConfirm.focus();
        document.body.style.overflow = 'hidden';
    }

    function hideModal() {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }, 300);
        pendingDeleteAction = null;
    }

    modalCancel.addEventListener('click', hideModal);
    
    modalConfirm.addEventListener('click', () => {
        if (pendingDeleteAction) {
            pendingDeleteAction();
        }
        hideModal();
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            hideModal();
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            hideModal();
        }
    });

    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            
            const todoId = e.target.getAttribute('data-id');
            const todoItem = e.target.closest('.todo-item');
            
            pendingDeleteAction = async () => {
                button.disabled = true;
                button.textContent = 'Deleting...';
                
                try {
                    const response = await fetch(`/delete/${todoId}`, { method: 'GET' });
                    if (response.ok) {
                        todoItem.style.transform = 'translateX(-100%)';
                        todoItem.style.opacity = '0';
                        setTimeout(() => location.reload(), 300);
                    } else {
                        throw new Error('Failed to delete');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    showCustomAlert('Failed to delete task', 'error');
                    button.disabled = false;
                    button.textContent = 'Delete';
                }
            };
            
            showModal();
        });
    });

    document.querySelectorAll('.edit-form').forEach(form => {
        const input = form.querySelector('.edit-input');
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                form.submit();
            }
        });

        input.addEventListener('focus', () => {
            input.select();
        });

        form.addEventListener('submit', (e) => {
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Updating...';
        });
    });

    document.querySelectorAll('.todo-item').forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
        item.classList.add('fade-in');
    });
});

function togglePassword(inputId) {
    const passwordInput = document.getElementById(inputId);
    const toggleIcon = passwordInput.parentElement.querySelector('.password-toggle');
    const eyeVisible = toggleIcon.querySelectorAll('.eye-visible');
    const eyeHidden = toggleIcon.querySelectorAll('.eye-hidden');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeVisible.forEach(path => path.style.display = 'block');
        eyeHidden.forEach(path => path.style.display = 'none');
    } else {
        passwordInput.type = 'password';
        eyeVisible.forEach(path => path.style.display = 'none');
        eyeHidden.forEach(path => path.style.display = 'block');
    }
}

function showCustomAlert(message, type = 'info') {
    const existingAlert = document.querySelector('.custom-alert');
    if (existingAlert) {
        existingAlert.remove();
    }

    const alertDiv = document.createElement('div');
    alertDiv.className = `custom-alert custom-alert-${type}`;
    alertDiv.innerHTML = `
        <div class="alert-content">
            <div class="alert-icon">
                ${type === 'error' ? 
                    '<svg viewBox="0 0 24 24" width="20" height="20"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none"/><line x1="15" y1="9" x2="9" y2="15" stroke="currentColor" stroke-width="2"/><line x1="9" y1="9" x2="15" y2="15" stroke="currentColor" stroke-width="2"/></svg>' :
                    '<svg viewBox="0 0 24 24" width="20" height="20"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none"/><path d="m9 12 2 2 4-4" stroke="currentColor" stroke-width="2" fill="none"/></svg>'
                }
            </div>
            <span class="alert-message">${message}</span>
            <button class="alert-close" onclick="this.parentElement.parentElement.remove()">
                <svg viewBox="0 0 24 24" width="16" height="16">
                    <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2"/>
                    <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2"/>
                </svg>
            </button>
        </div>
    `;

    document.body.appendChild(alertDiv);
    setTimeout(() => alertDiv.classList.add('show'), 10);

    setTimeout(() => {
        if (alertDiv.parentElement) {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 300);
        }
    }, 5000);
}

function showClearAllModal() {
    const modal = document.getElementById('clearAllModal');
    const cancelBtn = document.getElementById('clearAllCancel');
    const confirmBtn = document.getElementById('clearAllConfirm');
    
    modal.style.display = 'flex';
    setTimeout(() => modal.classList.add('show'), 10);
    
    cancelBtn.onclick = () => {
        modal.classList.remove('show');
        setTimeout(() => modal.style.display = 'none', 300);
    };
    
    confirmBtn.onclick = async () => {
        try {
            confirmBtn.disabled = true;
            confirmBtn.textContent = 'Clearing...';
            
            const response = await fetch('/clear_all_completed', { method: 'GET' });
            if (response.ok) {
                showCustomAlert('All completed tasks cleared!', 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                throw new Error('Failed to clear tasks');
            }
        } catch (error) {
            console.error('Error:', error);
            showCustomAlert('Failed to clear tasks', 'error');
            confirmBtn.disabled = false;
            confirmBtn.textContent = 'Clear All';
        }
        
        modal.classList.remove('show');
        setTimeout(() => modal.style.display = 'none', 300);
    };
    
    modal.onclick = (e) => {
        if (e.target === modal) {
            modal.classList.remove('show');
            setTimeout(() => modal.style.display = 'none', 300);
        }
    };
}