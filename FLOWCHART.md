# Mumzworld Assistant - Application Flowchart

## How the Application Functions

```mermaid
flowchart TD
    A["🚀 User Opens App"] --> B["📱 Select Language<br/>English/Arabic/Both"]
    B --> C["👀 Display Welcome Content<br/>Title, Slogans, Tagline"]
    C --> D["📝 User Enters Baby Concern<br/>Text Area Input"]
    D --> E{"Arabic Translation<br/>Checked?"}
    E -->|Yes| F["☑️ Show Arabic Response<br/>Option Selected"]
    E -->|No| G["⬜ English Only"]
    F --> H["🔵 Click Button<br/>Get Recommendations"]
    G --> H
    H --> I{"User Input<br/>Valid?"}
    I -->|No| J["⚠️ Warning:<br/>Please type something"]
    I -->|Yes| K["⏳ Loading Spinner<br/>Analyzing needs..."]
    J --> D
    K --> L["🤖 Call Groq API<br/>llama-3.3-70b-versatile<br/>With System Prompt"]
    L --> M["📤 Send Prompt to AI:<br/>Expert Shopping Assistant Role<br/>User's Baby Situation<br/>Product Categories Request"]
    M --> N{"Translation<br/>Needed?"}
    N -->|Yes| O["🌐 AI Generates Response<br/>English + Arabic<br/>With Separator"]
    N -->|No| P["🌐 AI Generates<br/>English Response Only"]
    O --> Q["✨ Display Success Message"]
    P --> Q
    Q --> R["💝 Render Styled Container<br/>White Box with Pink Border<br/>Black Text"]
    R --> S["📋 Show Recommendations:<br/>- Product Categories<br/>- Why Each Item<br/>- Safety Notes if Needed"]
    S --> T["✅ User Reviews<br/>Product Ideas"]
    T --> U["🛒 User Explores on Mumzworld"]
    
    style A fill:#FFB6D9
    style B fill:#FF69B4
    style H fill:#FF1493
    style L fill:#FF69B4
    style Q fill:#90EE90
    style T fill:#FFB6D9
```

## Process Flow Overview

### Stage 1: Initialization & Language Selection
- User opens the Streamlit application
- Language selector appears at the top (English/Arabic/Both)
- Based on selection, appropriate content is displayed

### Stage 2: Content Display
- Welcome message with emoji animations
- Tagline and description
- Input box appears for user to enter their concern

### Stage 3: User Input & Configuration
- User types their baby-related concern
- Optional checkbox to include Arabic translation in response
- Submit button activated

### Stage 4: Input Validation
- App checks if text area has content
- If empty, warning message shown
- If valid, proceeds to API call

### Stage 5: AI Processing via Groq API
- System sends user's concern to Groq API
- Model: `llama-3.3-70b-versatile`
- AI acts as expert shopping assistant for Mumzworld
- AI generates 3-5 product category recommendations

### Stage 6: Response Generation
- If translation requested: AI provides English + Arabic versions
- If English only: Single language response
- Includes product explanations and safety notes when needed

### Stage 7: Display & User Action
- Success message shown
- Response rendered in styled white container with pink border
- User reviews recommendations
- User can explore products on Mumzworld

## Key Components

| Component | Purpose |
|-----------|---------|
| **Language Selector** | Enables bilingual support (EN/AR) |
| **Text Area** | Captures user's baby concern |
| **Checkbox** | Enables/disables Arabic translation |
| **Submit Button** | Triggers API call |
| **Groq API Integration** | Provides AI-powered recommendations |
| **Styling Container** | Pink theme with responsive design |
| **Loading Spinner** | Indicates processing status |

## Error Handling

- **Empty Input**: Warning message prompting user to enter text
- **API Errors**: User-friendly error messages displayed
- **Network Issues**: Caught and displayed gracefully

---

Generated: April 29, 2026
