# 📱 SIGMA-NEX GUI Guide

## Overview

L'interfaccia grafica di SIGMA-NEX fornisce un'esperienza utente moderna e intuitiva, progettata specificamente per l'uso medico e di emergenza.

## Getting Started

### Launching the GUI

```bash
# Avvia interfaccia grafica
sigma gui

# Con tema specifico
sigma gui --theme dark

# Modalità fullscreen
sigma gui --fullscreen

# Con scala personalizzata
sigma gui --scale-factor 1.2
```

### First Run Setup

Al primo avvio, la GUI ti guiderà attraverso:
1. **Configurazione iniziale** - Impostazioni base del sistema
2. **Download modelli** - Scaricamento modelli AI necessari
3. **Test connessione** - Verifica Ollama e componenti
4. **Personalizzazione** - Tema, lingua, preferenze

## Interface Overview

### Main Window Layout

```
┌─────────────────────────────────────────────────────────────┐
│  SIGMA-NEX - Medical AI Assistant                  [_][□][X] │
├─────────────────────────────────────────────────────────────┤
│ [File] [Tools] [Settings] [Help]                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │               CONVERSATION AREA                     │   │
│  │                                                     │   │
│  │  🤖 AI: Ciao! Come posso aiutarti oggi?           │   │
│  │                                                     │   │
│  │  👤 User: Come disinfettare una ferita?            │   │
│  │                                                     │   │
│  │  🤖 AI: Per disinfettare una ferita...             │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Scrivi la tua domanda qui...                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [🚨 Emergency] [🔄 Clear] [💾 Save] [📋 Copy] [⚙️ Settings] │
│                                                             │
│  Status: ✅ Connected | Model: Mistral | 🌐 Online          │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Menu Bar**: File operations, tools, settings, help
2. **Conversation Area**: Chat history with scrollable content
3. **Input Field**: Text input with auto-resize and formatting
4. **Action Buttons**: Quick access to common functions
5. **Status Bar**: Connection status, model info, system state

## Core Features

### Chat Interface

#### Conversation Flow

```python
# Example conversation flow
User: "Come misurare la pressione arteriosa?"

AI: """
🩺 **MISURAZIONE PRESSIONE ARTERIOSA**

**Strumenti necessari:**
• Sfigmomanometro (bracciale)
• Stetoscopio
• Superficie piana

**Procedura:**
1. Far sedere il paziente per 5 minuti
2. Posizionare il bracciale 2-3 cm sopra il gomito
3. Gonfiare fino a 180-200 mmHg
4. Sgonfiare lentamente (2-3 mmHg/secondo)
5. Annotare pressione sistolica e diastolica

**Valori normali:**
• Sistolica: 90-120 mmHg
• Diastolica: 60-80 mmHg

⚠️ Consultare un medico se valori persistentemente alti
"""
```

#### Message Types

- **👤 User Messages**: Queries and questions
- **🤖 AI Responses**: Standard AI responses
- **🏥 Medical Responses**: Enhanced medical content with icons
- **🚨 Emergency Alerts**: Critical medical information
- **ℹ️ System Messages**: Status updates and notifications
- **⚠️ Warnings**: Important safety information

### Emergency Mode

#### Quick Access Emergency Button

```
🚨 EMERGENCY MODE
├── 🆘 Cardiac Arrest (RCP)
├── 🩸 Severe Bleeding
├── 🫁 Choking/Airway Obstruction  
├── 🔥 Burns
├── 💊 Poisoning
├── 🧠 Stroke Signs
├── 💔 Heart Attack
└── 🤕 Trauma Assessment
```

#### Emergency Interface

When emergency mode is activated:
- **Priority Processing**: Faster response times
- **Structured Protocols**: Step-by-step emergency procedures
- **Visual Aids**: Icons and formatting for clarity
- **Quick Actions**: One-click access to protocols
- **Emergency Contacts**: Quick access to emergency numbers

### Medical Tools Integration

#### Built-in Medical Calculators

```
🧮 MEDICAL CALCULATORS
├── BMI Calculator
├── Dosage Calculator
├── IV Flow Rate
├── Body Surface Area
├── Creatinine Clearance
├── APGAR Score
├── Glasgow Coma Scale
└── Pain Scale Assessment
```

#### Drug Database Integration

```
💊 DRUG INFORMATION
├── Search Medications
├── Dosage Guidelines
├── Interactions Checker
├── Side Effects
├── Contraindications
├── Generic/Brand Names
└── Pregnancy Categories
```

## Advanced Features

### Multi-Language Support

```python
# Language switching in GUI
Languages:
├── 🇮🇹 Italiano (Primary)
├── 🇺🇸 English
├── 🇪🇸 Español  
├── 🇫🇷 Français
├── 🇩🇪 Deutsch
├── 🇵🇹 Português
├── 🇷🇺 Русский
└── 🇨🇳 中文
```

### Conversation Management

#### Save and Load Conversations

```bash
# Save current conversation
File → Save Conversation → medical_consultation_2024.txt

# Load previous conversation
File → Load Conversation → select file

# Export formats
├── Plain Text (.txt)
├── Rich Text (.rtf)
├── PDF Report (.pdf)
├── JSON Data (.json)
└── Medical Report (.html)
```

#### Conversation Templates

```
📋 CONVERSATION TEMPLATES
├── 🏥 Medical Consultation
├── 🚨 Emergency Assessment
├── 💊 Medication Review
├── 🔬 Symptom Analysis
├── 🏃 First Aid Training
└── 🧑‍⚕️ Clinical Guidelines
```

### Customization Options

#### Theme Customization

```python
# Available themes
Themes:
├── 🌙 Dark Mode (Default)
├── ☀️ Light Mode
├── 🏥 Medical Blue
├── 🚨 Emergency Red
├── 🌿 Nature Green
├── 🎨 Custom Theme
└── 🔄 Auto (System)
```

#### Interface Customization

```yaml
# GUI Configuration
gui:
  theme: "dark"
  font_family: "Segoe UI"
  font_size: 12
  scaling: 1.0
  
  chat:
    message_spacing: 10
    timestamp_visible: true
    user_avatar: "👤"
    ai_avatar: "🤖"
    
  colors:
    primary: "#2B579A"
    secondary: "#E7F3FF"
    accent: "#FF6B6B"
    success: "#51CF66"
    warning: "#FFD93D"
    error: "#FF6B6B"
```

## Accessibility Features

### Visual Accessibility

- **High Contrast Mode**: Better visibility for visually impaired
- **Font Scaling**: Adjustable text size (50%-200%)
- **Color Blind Support**: Alternative color schemes
- **Screen Reader Compatible**: NVDA, JAWS, VoiceOver support

### Input Accessibility

- **Keyboard Navigation**: Full keyboard control
- **Voice Input**: Speech-to-text integration (planned)
- **Touch Support**: Tablet and touch screen friendly
- **One-Handed Mode**: Optimized for mobile use

### Medical Accessibility

- **Simplified Language**: Plain language medical explanations
- **Visual Icons**: Icon-based navigation for medical procedures
- **Audio Alerts**: Sound notifications for emergencies
- **Print Support**: Easy printing of medical information

## Integration Features

### External Tool Integration

#### Medical Devices (Planned)

```
🏥 DEVICE INTEGRATION
├── 🩺 Digital Stethoscope
├── 📱 Blood Pressure Monitor
├── 🌡️ Digital Thermometer
├── 📊 Pulse Oximeter
├── 🔬 Glucometer
└── ⚖️ Digital Scale
```

#### File System Integration

```python
# File operations
File Menu:
├── 📂 Open Medical Record
├── 💾 Save Consultation
├── 📄 Export Report
├── 🖨️ Print Summary
├── 📧 Email Report
├── ☁️ Cloud Sync (Planned)
└── 🔒 Encrypt File
```

### Workflow Integration

#### Hospital Information Systems (Planned)

- **HL7 FHIR**: Standard medical data exchange
- **EMR Integration**: Electronic Medical Records
- **DICOM Support**: Medical imaging integration
- **Lab Results**: Laboratory data integration

## Keyboard Shortcuts

### Global Shortcuts

```
Ctrl+N      New Conversation
Ctrl+O      Open Conversation
Ctrl+S      Save Conversation
Ctrl+Q      Quit Application
Ctrl+,      Open Settings
F1          Help
F11         Toggle Fullscreen
Esc         Exit Emergency Mode
```

### Chat Shortcuts

```
Enter       Send Message
Shift+Enter Line Break
Ctrl+L      Clear Conversation
Ctrl+C      Copy Last Response
Ctrl+V      Paste
Ctrl+Z      Undo
Ctrl+Y      Redo
Ctrl+A      Select All
Ctrl+F      Find in Conversation
```

### Emergency Shortcuts

```
F9          Emergency Mode
Ctrl+E      Emergency Protocols
Ctrl+1-9    Quick Emergency Actions
Alt+M       Medical Calculator
Alt+D       Drug Database
Alt+H       Emergency Contacts
```

## Settings and Configuration

### Preferences Window

```
⚙️ SETTINGS
├── 🎨 Appearance
│   ├── Theme Selection
│   ├── Font Settings
│   ├── Color Customization
│   └── Layout Options
├── 🤖 AI Model
│   ├── Model Selection
│   ├── Response Length
│   ├── Creativity Level
│   └── Medical Mode
├── 🌐 Language
│   ├── Interface Language
│   ├── Medical Terminology
│   ├── Translation Options
│   └── Regional Settings
├── 🔒 Privacy
│   ├── Data Collection
│   ├── Conversation Logging
│   ├── Anonymization
│   └── Audit Settings
├── 🚨 Emergency
│   ├── Quick Access Setup
│   ├── Emergency Contacts
│   ├── Protocol Preferences
│   └── Alert Settings
└── 🔧 Advanced
    ├── Performance Options
    ├── Cache Settings
    ├── Network Configuration
    └── Debug Options
```

## Troubleshooting GUI Issues

### Common Problems

#### GUI Won't Start

```bash
# Check dependencies
python -c "import customtkinter; print('GUI OK')"

# Reset GUI settings
# Modify config.yaml: gui.reset true

# Start in safe mode
sigma gui --safe-mode
```

#### Display Issues

```bash
# Fix scaling issues
sigma gui --scale-factor 1.0

# Reset window size
# Modify config.yaml: gui.window_size [800, 600]

# Check display settings
# Diagnose manually display
```

#### Performance Issues

```bash
# Disable animations
# Modify config.yaml: gui.animations false

# Reduce update frequency
# Modify config.yaml: gui.refresh_rate 30

# Enable hardware acceleration
# Modify config.yaml: gui.hardware_acceleration true
```

### Debug Mode

```bash
# Start GUI in debug mode
sigma gui --debug

# Enable verbose logging
# Modify config.yaml: gui.debug_logging true

# Show performance metrics
sigma gui --show-fps
```

## Tips and Best Practices

### Efficient Usage

1. **Use Templates**: Save time with conversation templates
2. **Keyboard Shortcuts**: Learn shortcuts for faster navigation
3. **Emergency Mode**: Practice emergency procedures
4. **Bookmarks**: Save frequently used medical information
5. **Batch Queries**: Ask multiple related questions together

### Medical Best Practices

1. **Always Verify**: Cross-reference critical medical information
2. **Emergency Priority**: Use emergency mode for urgent situations
3. **Document Everything**: Save important consultations
4. **Regular Updates**: Keep medical databases current
5. **Training**: Regular practice with emergency protocols

### Security Tips

1. **Private Mode**: Use private mode for sensitive information
2. **Secure Storage**: Encrypt saved conversations
3. **Regular Cleanup**: Clear cache and temporary files
4. **Access Control**: Limit access to medical information
5. **Audit Trail**: Monitor access to medical data

For GUI support:
- **User Guide**: https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/docs/guides/gui-guide.md
- **Video Tutorials**: https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/docs/guides/tutorials.md
- **Community**: https://github.com/SebastianMartinNS/SYGMA-NEX/discussions
- **Support**: rootedlab6@gmail.com
