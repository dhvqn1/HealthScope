"""
HealthScope Design System
Centralized theme configuration with colors, gradients, shadows, spacing, and typography.
"""

class HealthScopeTheme:
    """
    Premium design system for HealthScope dashboard
    """
    
    # Typography
    FONT_FAMILY = "'Poppins', 'Inter', sans-serif"
    FONT_SIZES = {
        'xs': '0.75rem',
        'sm': '0.875rem',
        'base': '1rem',
        'lg': '1.125rem',
        'xl': '1.25rem',
        '2xl': '1.5rem',
        '3xl': '1.875rem',
        '4xl': '2.25rem',
        '5xl': '3rem',
    }
    
    # Spacing System (padding, margin)
    SPACING = {
        'xs': '0.25rem',
        'sm': '0.5rem',
        'md': '1rem',
        'lg': '1.5rem',
        'xl': '2rem',
        '2xl': '3rem',
        '3xl': '4rem',
    }
    
    # Border Radius
    RADIUS = {
        'sm': '0.375rem',
        'md': '0.5rem',
        'lg': '0.75rem',
        'xl': '1rem',
        '2xl': '1.5rem',
        'full': '9999px',
    }
    
    # Shadow Levels
    SHADOWS = {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.15)',
    }
    
    # Homepage Theme (Healthcare Teal/Blue)
    HOME = {
        'primary': '#1CC5DC',
        'secondary': '#1A5F7A',
        'background': '#F3FFFD',
        'text': '#093A44',
        'white': '#FFFFFF',
        'gradient': 'linear-gradient(135deg, #1CC5DC 0%, #1A5F7A 100%)',
        'gradient_light': 'linear-gradient(135deg, #F3FFFD 0%, #E0F7FA 100%)',
    }
    
    # Heart Disease Theme (Red)
    HEART = {
        'primary': '#FF6B6B',
        'secondary': '#C21010',
        'background': '#FFF0F3',
        'gradient': 'linear-gradient(135deg, #FF6B6B 0%, #C21010 100%)',
        'gradient_light': 'linear-gradient(135deg, #FFF0F3 0%, #FFE0E6 100%)',
        'text': '#8B0000',
        'light': '#FFE5E5',
    }
    
    # Diabetes Theme (Indigo)
    DIABETES = {
        'primary': '#6C63FF',
        'secondary': '#4B49FF',
        'background': '#F2F2FF',
        'gradient': 'linear-gradient(135deg, #6C63FF 0%, #4B49FF 100%)',
        'gradient_light': 'linear-gradient(135deg, #F2F2FF 0%, #E6E6FF 100%)',
        'text': '#3A38B2',
        'light': '#E8E7FF',
    }
    
    # PCOS Theme (Pink)
    PCOS = {
        'primary': '#FFB6C1',
        'secondary': '#FF5CA8',
        'background': '#FFF6FB',
        'gradient': 'linear-gradient(135deg, #FFB6C1 0%, #FF5CA8 100%)',
        'gradient_light': 'linear-gradient(135deg, #FFF6FB 0%, #FFE5F0 100%)',
        'text': '#C7417B',
        'light': '#FFEEF6',
    }
    
    # Risk Level Colors
    RISK_COLORS = {
        'low': '#10B981',      # Green
        'medium': '#F59E0B',   # Amber
        'high': '#EF4444',     # Red
        'critical': '#DC2626', # Dark Red
    }
    
    # Chart Colors (for each theme)
    CHART_COLORS = {
        'home': ['#1CC5DC', '#1A5F7A', '#5DD9ED', '#2C8FA3', '#86E3F5'],
        'heart': ['#FF6B6B', '#C21010', '#FF8585', '#A61C1C', '#FFA5A5'],
        'diabetes': ['#6C63FF', '#4B49FF', '#8E87FF', '#3D3BE6', '#AFA9FF'],
        'pcos': ['#FFB6C1', '#FF5CA8', '#FFC9D1', '#FF3D94', '#FFD6DF'],
    }
    
    @staticmethod
    def get_glassmorphism_style(background_color='rgba(255, 255, 255, 0.25)', blur='10px'):
        """Generate glassmorphism CSS properties"""
        return f"""
            background: {background_color};
            backdrop-filter: blur({blur});
            -webkit-backdrop-filter: blur({blur});
            border: 1px solid rgba(255, 255, 255, 0.18);
            box-shadow: {HealthScopeTheme.SHADOWS['glass']};
        """
    
    @staticmethod
    def get_hover_animation():
        """Get CSS for hover scale animation"""
        return """
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            &:hover {
                transform: translateY(-4px) scale(1.02);
                box-shadow: {HealthScopeTheme.SHADOWS['xl']};
            }
        """
    
    @staticmethod
    def get_shimmer_keyframes():
        """Get shimmer loading animation keyframes"""
        return """
            @keyframes shimmer {
                0% { background-position: -1000px 0; }
                100% { background-position: 1000px 0; }
            }
        """
    
    @staticmethod
    def get_fade_in_animation(delay='0s'):
        """Get fade-in animation"""
        return f"""
            animation: fadeIn 0.6s ease-in-out {delay} both;
            @keyframes fadeIn {{
                from {{
                    opacity: 0;
                    transform: translateY(20px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
        """
    
    @staticmethod
    def get_ripple_effect():
        """Get CSS for ripple effect on click"""
        return """
            position: relative;
            overflow: hidden;
            &::after {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 0;
                height: 0;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.5);
                transform: translate(-50%, -50%);
                transition: width 0.6s, height 0.6s;
            }
            &:active::after {
                width: 300px;
                height: 300px;
            }
        """
