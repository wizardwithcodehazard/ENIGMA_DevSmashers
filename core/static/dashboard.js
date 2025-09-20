// Enhanced Dashboard JavaScript with Animations and Interactions

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
});

// Smooth scroll for anchor links
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

// Add loading states to buttons
document.querySelectorAll('button, .btn').forEach(button => {
    button.addEventListener('click', function() {
        if (!this.classList.contains('loading')) {
            this.classList.add('loading');
            setTimeout(() => {
                this.classList.remove('loading');
            }, 2000);
        }
    });
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all sections for fade-in effect
document.querySelectorAll('section').forEach(section => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(20px)';
    section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(section);
});

// Enhanced Chart.js configuration
const container = document.getElementById('stabilityChartContainer');
const score = container ? parseInt(container.dataset.score) : 0;

// Render Stability Score chart with enhanced styling
const ctx = document.getElementById('stabilityChart');
if (ctx) {
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Stability', 'Remaining'],
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: [
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(226, 232, 240, 0.8)'
                ],
                borderColor: [
                    'rgba(102, 126, 234, 1)',
                    'rgba(226, 232, 240, 1)'
                ],
                borderWidth: 2,
                hoverBackgroundColor: [
                    'rgba(102, 126, 234, 0.9)',
                    'rgba(226, 232, 240, 0.9)'
                ]
            }]
        },
        options: {
            cutout: '75%',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    displayColors: false
                }
            },
            animation: {
                animateRotate: true,
                animateScale: true,
                duration: 2000,
                easing: 'easeOutQuart'
            }
        }
    });
}

// Add hover effects to cards
document.querySelectorAll('.action-card, .post-card, .goal-item').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-2px)';
        this.style.boxShadow = '0 10px 25px rgba(0, 0, 0, 0.15)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
    });
});

// Add ripple effect to buttons
document.querySelectorAll('button, .btn').forEach(button => {
    button.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        this.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
});

// Add CSS for ripple effect
const style = document.createElement('style');
style.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    button, .btn {
        position: relative;
        overflow: hidden;
    }
`;
document.head.appendChild(style);

// Add progress bar animations
document.querySelectorAll('.goal-progress-bar').forEach(bar => {
    const width = bar.style.width || bar.getAttribute('data-width') || '0%';
    bar.style.width = '0%';
    setTimeout(() => {
        bar.style.width = width;
    }, 500);
});

// Add counter animation for stats
function animateCounter(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const current = Math.floor(progress * (end - start) + start);
        element.textContent = current;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Animate stat counters
document.querySelectorAll('.stat-value').forEach(stat => {
    const finalValue = parseInt(stat.textContent);
    if (!isNaN(finalValue)) {
        stat.textContent = '0';
        setTimeout(() => {
            animateCounter(stat, 0, finalValue, 2000);
        }, 500);
    }
});

// Add typing effect for welcome message
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.innerHTML = '';
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    type();
}

// Apply typing effect to welcome message if it exists
const welcomeMessage = document.querySelector('header h1');
if (welcomeMessage) {
    const originalText = welcomeMessage.textContent;
    setTimeout(() => {
        typeWriter(welcomeMessage, originalText, 50);
    }, 1000);
}

// Add parallax effect to header
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const header = document.querySelector('header');
    if (header) {
        header.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});

// Add smooth transitions for all interactive elements
document.querySelectorAll('a, button, .btn, .card, .action-card, .post-card').forEach(element => {
    element.style.transition = 'all 0.3s ease';
});

// Add focus styles for accessibility
document.querySelectorAll('button, .btn, a').forEach(element => {
    element.addEventListener('focus', function() {
        this.style.outline = '2px solid rgba(102, 126, 234, 0.5)';
        this.style.outlineOffset = '2px';
    });
    
    element.addEventListener('blur', function() {
        this.style.outline = 'none';
    });
});

// Add keyboard navigation support
document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
    }
});

document.addEventListener('mousedown', () => {
    document.body.classList.remove('keyboard-navigation');
});

// Add CSS for keyboard navigation
const keyboardStyle = document.createElement('style');
keyboardStyle.textContent = `
    .keyboard-navigation *:focus {
        outline: 2px solid rgba(102, 126, 234, 0.5) !important;
        outline-offset: 2px !important;
    }
`;
document.head.appendChild(keyboardStyle);

// Performance optimization: Debounce scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Apply debounced scroll handler
const debouncedScrollHandler = debounce(() => {
    // Add any scroll-based functionality here
}, 10);

window.addEventListener('scroll', debouncedScrollHandler);

// Add loading skeleton for dynamic content
function createSkeletonLoader() {
    const skeleton = document.createElement('div');
    skeleton.className = 'skeleton-loader';
    skeleton.innerHTML = `
        <div class="skeleton-line"></div>
        <div class="skeleton-line short"></div>
        <div class="skeleton-line"></div>
    `;
    return skeleton;
}

// Add CSS for skeleton loader
const skeletonStyle = document.createElement('style');
skeletonStyle.textContent = `
    .skeleton-loader {
        padding: 1rem;
    }
    
    .skeleton-line {
        height: 1rem;
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
        border-radius: 4px;
        margin: 0.5rem 0;
    }
    
    .skeleton-line.short {
        width: 60%;
    }
    
    @keyframes loading {
        0% {
            background-position: 200% 0;
        }
        100% {
            background-position: -200% 0;
        }
    }
`;
document.head.appendChild(skeletonStyle);

console.log('🚀 Enhanced Dashboard JavaScript loaded successfully!');