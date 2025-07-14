# Binary Hand Gesture Converter

A real-time computer vision application that converts binary sequences to decimal numbers using hand gestures. Built with OpenCV and MediaPipe for accurate hand tracking and gesture recognition.

## 🎯 Overview

This application allows users to input binary digits using simple hand gestures and instantly convert them to decimal numbers. It's an interactive way to learn binary-decimal conversion while exploring computer vision technology.

## ✨ Features

- **Real-time Hand Tracking**: Uses MediaPipe for accurate hand landmark detection
- **Intuitive Gesture Controls**: Simple hand gestures for binary input
- **Live Visual Feedback**: Real-time display of gestures, binary sequence, and conversion results
- **Smart Timing Controls**: Prevents accidental rapid inputs with gesture timing
- **Debug Information**: Shows finger detection details for troubleshooting
- **Sequence Management**: Easy reset and new sequence functionality

## 🤚 Gesture Controls

| Gesture | Binary Value | Description |
|---------|-------------|-------------|
| ✊ **Fist** | `0` | All fingers down |
| ☝️ **One Finger** | `1` | Only index finger extended |
| ✋ **Open Palm** | **CONVERT** | 4-5 fingers extended - triggers conversion |

## 🛠️ Installation

### Prerequisites

Make sure you have Python 3.7+ installed on your system.

### Required Dependencies

```bash
pip install opencv-python mediapipe numpy
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

### Clone the Repository

```bash
git clone https://github.com/Rohan095/Binary_Converter.git
cd Binary_Converter
```

## 🚀 Usage

1. **Run the application**:
   ```bash
   python Binary_Converter.py
   ```

2. **Position your hand** in front of the webcam (ensure good lighting)

3. **Input binary digits**:
   - Show a **fist** to input `0`
   - Show **one finger** (index) to input `1`
   - Wait 1 second between each gesture

4. **Convert to decimal**:
   - Show an **open palm** to convert your binary sequence
   - The result will display for 5 seconds

5. **Start new sequence**:
   - Show a **fist** after conversion to reset and start a new sequence

6. **Exit**: Press `q` to quit the application

## 📱 Interface

The application window displays:
- **Current Gesture**: Real-time gesture detection
- **Binary Sequence**: Your current binary input
- **Conversion Result**: Decimal equivalent (shown for 5 seconds)
- **Debug Info**: Finger detection details
- **Instructions**: Quick reference guide

## 🔧 Technical Details

### Hand Gesture Recognition
- Uses MediaPipe's hand landmark detection
- Analyzes finger positions relative to MCP (metacarpophalangeal) joints
- Classifies gestures based on extended finger count and positions

### Gesture Classification Algorithm
```python
# Finger extension detection
if tip.y < mcp.y:  # Tip above MCP = extended finger
    fingers_up.append(1)
else:
    fingers_up.append(0)

# Gesture classification
total_fingers = sum(fingers_up)
if total_fingers == 0: return "fist"      # Binary 0
elif total_fingers == 1: return "one"     # Binary 1  
elif total_fingers >= 4: return "palm"    # Convert
```

### Key Parameters
- **Detection Confidence**: 0.7 (minimum confidence for hand detection)
- **Tracking Confidence**: 0.5 (minimum confidence for hand tracking)
- **Gesture Timing**: 1.0 second delay between digit inputs
- **Palm Timing**: 2.0 second delay between conversions

## 🎓 Educational Use

This project is perfect for:
- **Learning Binary Systems**: Interactive way to understand binary-decimal conversion
- **Computer Vision Education**: Hands-on experience with OpenCV and MediaPipe
- **Gesture Recognition**: Understanding landmark-based gesture classification
- **Real-time Processing**: Working with live video streams and real-time algorithms

## 🐛 Troubleshooting

### Common Issues

**Hand not detected:**
- Ensure good lighting conditions
- Keep hand within camera frame
- Check if webcam is working properly

**Gesture recognition issues:**
- Make clear, distinct gestures
- Wait for timing delays between gestures
- Check debug information for finger detection status

**Conversion not working:**
- Ensure you have input at least one binary digit
- Wait 2 seconds between palm gestures
- Check that palm gesture shows 4-5 fingers extended

## 📋 Example Usage

```
Input Sequence: 1011
Gestures: One → Fist → One → One → Palm
Result: Binary 1011 → Decimal 11
```

## 🔄 Future Enhancements

- Support for hexadecimal conversion
- Multiple hand detection
- Gesture customization options
- Voice feedback integration
- Mobile app version

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for hand tracking technology
- [OpenCV](https://opencv.org/) for computer vision tools
- Computer vision and gesture recognition research community

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section
2. Open an issue on GitHub
3. Contact the maintainer - rohanagrawal90456@gmail.com

---

**Made for interactive learning and computer vision exploration**
