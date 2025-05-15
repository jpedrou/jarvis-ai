class Globe {
    constructor() {
        this.canvas = document.getElementById('canvasOne');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.connections = [];
        this.numParticles = 100;
        this.centerX = this.canvas.width / 2;
        this.centerY = this.canvas.height / 2;
        this.radius = 80;
        
        // Cores futuristas
        this.colors = {
            particle: '255, 255, 255',      // Branco brilhante
            connection: '255, 255, 255',     // Linhas de conexão
            pulse: '200, 200, 200'          // Pulso mais suave
        };
        
        this.init();
        this.animate();
    }

    init() {
        // Criar partículas
        for (let i = 0; i < this.numParticles; i++) {
            const theta = Math.random() * 2 * Math.PI;
            const phi = Math.random() * Math.PI;
            
            this.particles.push({
                x: this.radius * Math.sin(phi) * Math.cos(theta),
                y: this.radius * Math.sin(phi) * Math.sin(theta),
                z: this.radius * Math.cos(phi),
                speed: 0.005 + Math.random() * 0.005,
                size: 2 + Math.random() * 2,
                pulse: Math.random() * 2 * Math.PI
            });
        }
    }

    drawConnections() {
        // Desenhar conexões entre partículas próximas
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const dz = this.particles[i].z - this.particles[j].z;
                const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
                
                if (distance < this.radius * 0.5) {
                    const alpha = (1 - distance / (this.radius * 0.5)) * 0.2;
                    this.ctx.strokeStyle = `rgba(${this.colors.connection}, ${alpha})`;
                    this.ctx.beginPath();
                    this.ctx.moveTo(
                        this.particles[i].x2d,
                        this.particles[i].y2d
                    );
                    this.ctx.lineTo(
                        this.particles[j].x2d,
                        this.particles[j].y2d
                    );
                    this.ctx.stroke();
                }
            }
        }
    }

    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Atualizar e desenhar partículas
        for (let particle of this.particles) {
            // Rotação
            const x = particle.x;
            const z = particle.z;
            particle.x = x * Math.cos(particle.speed) - z * Math.sin(particle.speed);
            particle.z = z * Math.cos(particle.speed) + x * Math.sin(particle.speed);
            
            // Projeção 2D
            const scale = 200 / (200 + particle.z);
            particle.x2d = particle.x * scale + this.centerX;
            particle.y2d = particle.y * scale + this.centerY;
            
            // Efeito de pulso
            particle.pulse += 0.05;
            const pulseSize = particle.size + Math.sin(particle.pulse) * 1;
            
            // Desenhar partícula com brilho
            const alpha = ((particle.z + this.radius) / (2 * this.radius)) * 0.8 + 0.2;
            
            // Efeito de brilho
            const gradient = this.ctx.createRadialGradient(
                particle.x2d, particle.y2d, 0,
                particle.x2d, particle.y2d, pulseSize * 2
            );
            gradient.addColorStop(0, `rgba(${this.colors.particle}, ${alpha})`);
            gradient.addColorStop(1, `rgba(${this.colors.pulse}, 0)`);
            
            this.ctx.fillStyle = gradient;
            this.ctx.beginPath();
            this.ctx.arc(particle.x2d, particle.y2d, pulseSize, 0, Math.PI * 2);
            this.ctx.fill();
        }
        
        this.drawConnections();
        requestAnimationFrame(() => this.draw());
    }

    animate() {
        this.draw();
    }
}

// Inicializar o globo
document.addEventListener('DOMContentLoaded', () => {
    new Globe();
});