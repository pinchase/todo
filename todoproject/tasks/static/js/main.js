// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // Update completed tasks count on dashboard
    updateCompletedCount();
});

/**
 * Toggle task completion status
 * @param {number} taskId - The ID of the task to toggle
 */
function toggleTask(taskId) {
    // Get the checkbox element
    const checkbox = document.getElementById(`task-${taskId}`);
    const taskCard = checkbox.closest('.task-card');

    // Add visual feedback immediately
    taskCard.style.transition = 'opacity 0.3s ease';

    if (checkbox.checked) {
        taskCard.classList.add('completed');
    } else {
        taskCard.classList.remove('completed');
    }

    // Send request to server
    window.location.href = `/toggle/${taskId}/`;
}

/**
 * Delete task with confirmation
 * @param {number} taskId - The ID of the task to delete
 */
function deleteTask(taskId) {
    // Get the task card to find the task title
    const taskCard = document.querySelector(`[data-task-id="${taskId}"]`);
    const taskTitle = taskCard.querySelector('.task-title').textContent;

    // Confirm deletion
    const confirmed = confirm(`Are you sure you want to delete "${taskTitle}"?`);

    if (confirmed) {
        // Add fade-out animation
        taskCard.style.transition = 'all 0.3s ease';
        taskCard.style.opacity = '0';
        taskCard.style.transform = 'translateX(-20px)';

        // Redirect to delete URL after animation
        setTimeout(() => {
            window.location.href = `/delete/${taskId}/`;
        }, 300);
    }
}

/**
 * Update the completed tasks counter
 */
function updateCompletedCount() {
    const completedCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    const completedCountElement = document.getElementById('completed-count');

    if (completedCountElement) {
        completedCountElement.textContent = completedCheckboxes.length;
    }
}

/**
 * Form validation for add/edit task forms
 */
const taskForms = document.querySelectorAll('#addTaskForm, #editTaskForm');
taskForms.forEach(form => {
    form.addEventListener('submit', function(e) {
        const titleInput = form.querySelector('#title');
        const title = titleInput.value.trim();

        if (title === '') {
            e.preventDefault();
            alert('Task title is required!');
            titleInput.focus();
            return false;
        }

        if (title.length > 200) {
            e.preventDefault();
            alert('Task title must be less than 200 characters!');
            titleInput.focus();
            return false;
        }
    });
});

/**
 * Add smooth scroll behavior for navigation
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});