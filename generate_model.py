import mlflow
import mlflow.pyfunc
import os

class DummyModel(mlflow.pyfunc.PythonModel):
    def predict(self, context, model_input):
        return model_input

if __name__ == "__main__":
    model_path = "/app/saved_model"
    
    if not os.path.exists(model_path):
        print("[*] Generating minimal MLflow pyfunc model...")
        mlflow.pyfunc.save_model(
            path=model_path,
            python_model=DummyModel()
        )
        print(f"[+] Model successfully saved to {model_path}")
    else:
        print("[*] Model directory already exists.")