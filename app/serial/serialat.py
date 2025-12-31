import serial
import threading
import queue
import time

class SerialReader:
    def __init__(self, port_name, baud_rate, callback = None):
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.serial_queue = queue.Queue()
        self.callback = callback
        self.running = False
        self.thread = None

    def _reader_thread(self):
        """Hilo que lee datos continuamente del puerto serial."""
        try:
            ser = serial.Serial(self.port_name, self.baud_rate, timeout=1)
            print(f"Serial port {self.port_name} opened successfully.")

            while self.running:
                try:
                    line = ser.readline()
                    if line:
                        decoded_line = line.decode('utf-8').strip()
                        self.serial_queue.put(decoded_line)
                        if self.callback:
                            self.callback(decoded_line)

                except serial.SerialException as e:
                    print(f"Serial error: {e}")
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    break
        except serial.SerialException as e:
            print(f"Failed to open serial port {self.port_name}: {e}")
        finally:
            if 'ser' in locals() and ser.is_open:
                ser.close()
                print(f"Serial port {self.port_name} closed.")

    def start(self):
        """Inicia el hilo lector."""
        print("Serial reader thread started.")

        self.running = True
        self.thread = threading.Thread(target=self._reader_thread, daemon=True)
        self.thread.start()
        print("Serial reader thread started.")

    def stop(self):
        """Detiene el hilo lector."""
        self.running = False
        if self.thread is not None:
            self.thread.join()
        print("Serial reader thread stopped.")

    def get_data(self):
        """Obtiene datos desde la cola si existen."""
        if not self.serial_queue.empty():
            return self.serial_queue.get()
        return None

    def run_main_loop(self):
        """Loop principal que procesa datos recibidos."""
        print("Main program running. Press Ctrl+C to exit.")
        try:
            while True:
                data = self.get_data()
                if data:
                    print(f"Received in main thread: {data}")
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("\nExit signal received. Stopping...")
        finally:
            self.stop()
            print("Program terminated.")


# --- Main execution ---
if __name__ == '__main__':
    SERIAL_PORT = 'COM4'   # Cambia según tu sistema
    BAUD_RATE = 9600

    reader = SerialReader(SERIAL_PORT, BAUD_RATE)
    reader.start()
    reader.run_main_loop()