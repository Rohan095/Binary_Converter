import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

class HandGestureRecognizer:
    def __init__(self):
        self.hands = mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.binary_sequence = ""
        self.last_gesture_time = time.time()
        self.last_palm_time = 0  # Track when palm was last shown
        self.converted = False
        self.debug_info = ""  # Add debug information
        self.conversion_result = ""  # Store conversion result for display
        self.result_display_time = 0  # Track when to show result
        
    def classify_gesture(self, landmarks):
        """Classify the hand gesture with optimal gestures"""
        # Get landmark positions
        thumb_tip = landmarks[4]
        thumb_mcp = landmarks[2]
        index_tip = landmarks[8]
        index_mcp = landmarks[5]
        middle_tip = landmarks[12]
        middle_mcp = landmarks[9]
        ring_tip = landmarks[16]
        ring_mcp = landmarks[13]
        pinky_tip = landmarks[20]
        pinky_mcp = landmarks[17]
        wrist = landmarks[0]
        
        # Count extended fingers (tip above MCP joint)
        fingers_up = []
        
        # Thumb (different logic - check if tip is to the right/left of MCP)
        if thumb_tip.x > thumb_mcp.x:  # Right hand
            fingers_up.append(1)
        else:
            fingers_up.append(0)
            
        # Other fingers (check if tip is above MCP)
        finger_tips = [index_tip, middle_tip, ring_tip, pinky_tip]
        finger_mcps = [index_mcp, middle_mcp, ring_mcp, pinky_mcp]
        
        for tip, mcp in zip(finger_tips, finger_mcps):
            if tip.y < mcp.y:  # Tip above MCP = extended
                fingers_up.append(1)
            else:
                fingers_up.append(0)
        
        total_fingers = sum(fingers_up)
        
        # Debug: Store finger information
        self.debug_info = f"Fingers up: {fingers_up} | Total: {total_fingers}"
        
        # Optimal gesture classification
        if total_fingers == 0:
            return "fist"  # All fingers down = 0
        elif total_fingers == 1 and fingers_up[1] == 1:  # Only index finger up
            return "one"  # Index finger up = 1
        elif total_fingers >= 4:  # 4 or 5 fingers up
            return "palm"  # Open palm = STOP
        else:
            return "unknown"
    
    def process_binary_input(self, gesture):
        """Process binary input - only convert on open palm"""
        current_time = time.time()
        
        if gesture == "palm":
            print(f"DEBUG: Palm detected! Binary sequence: '{self.binary_sequence}'")
            print(f"DEBUG: Time since last palm: {current_time - self.last_palm_time:.2f}s")
            
            # Prevent multiple rapid conversions
            if current_time - self.last_palm_time < 2.0:  # Wait 2 seconds between palm gestures
                return f"Wait {2.0 - (current_time - self.last_palm_time):.1f}s before next palm"
                
            self.last_palm_time = current_time
            
            if self.binary_sequence:
                try:
                    decimal_value = int(self.binary_sequence, 2)
                    result = f"Binary: {self.binary_sequence} -> Decimal: {decimal_value}"
                    self.converted = True
                    self.conversion_result = result  # Store for display
                    self.result_display_time = current_time  # Track when to show result
                    print(f"SUCCESS: {result}")
                    return result
                except ValueError:
                    return "Invalid binary sequence"
            else:
                return "No sequence! Show fist (0) or one finger (1) first, then palm to convert"
        
        elif gesture in ["fist", "one"]:
            print(f"DEBUG: {gesture} detected!")
            print(f"DEBUG: Time since last gesture: {current_time - self.last_gesture_time:.2f}s")
            
            # Add delay between digit inputs
            if current_time - self.last_gesture_time > 1.0:  # Reduced from 1.5 to 1.0 seconds
                if gesture == "fist":
                    # Reset sequence when fist is shown after a palm conversion
                    if self.converted:
                        self.binary_sequence = ""
                        self.converted = False
                        self.conversion_result = ""  # Clear result display
                        return "New sequence started. Added: 0 | Sequence: 0"
                    else:
                        self.binary_sequence += "0"
                elif gesture == "one":
                    self.binary_sequence += "1"
                    
                self.last_gesture_time = current_time
                result = f"Added: {self.binary_sequence[-1]} | Sequence: {self.binary_sequence}"
                print(f"SUCCESS: {result}")
                return result
            else:
                wait_time = 1.0 - (current_time - self.last_gesture_time)
                return f"Wait {wait_time:.1f}s before next gesture"
        
        return None

def main():
    cap = cv2.VideoCapture(0)
    recognizer = HandGestureRecognizer()
    
    print("BINARY TO DECIMAL CONVERTER:")
    print("Fist (all fingers down) = 0")
    print("One finger up (index) = 1") 
    print("Open palm = CONVERT to decimal")
    print("Show FIST after conversion to start new sequence")
    print("Press 'q' to quit")
    print("=" * 50)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = recognizer.hands.process(frame_rgb)
        
        gesture = "none"
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                gesture = recognizer.classify_gesture(hand_landmarks.landmark)
                
                binary_result = recognizer.process_binary_input(gesture)
                if binary_result:
                    print(binary_result)
        
        # Display info with more details
        cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Sequence: {recognizer.binary_sequence}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        cv2.putText(frame, f"Debug: {recognizer.debug_info}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        
        # Display conversion result if available
        if recognizer.conversion_result and (time.time() - recognizer.result_display_time) < 5.0:
            cv2.putText(frame, f"RESULT: {recognizer.conversion_result}", (10, 150), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Instructions
        cv2.putText(frame, "Fist=0, One Finger=1, Open Palm=CONVERT", (10, frame.shape[0] - 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow("Binary Hand Gestures", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()