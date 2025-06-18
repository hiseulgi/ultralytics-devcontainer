"""Main Ultralytics Yolo Trainer

Usage:
python src/train.py \
    --model yolo11s.pt \
    --data data/bag-pkt/data.yaml \
    --epochs 50 \
    --imgsz 640 \
    --batch 16 \
    --project pkt_yolov11s
"""

import rootutils

ROOT = rootutils.autosetup()


from pathlib import Path
from ultralytics import YOLO, settings
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Train YOLO model")
    parser.add_argument(
        "--model",
        type=str,
        default="yolo11s.pt",
        help="Path to YOLO model (default: yolo11s.pt)",
    )
    parser.add_argument(
        "--data",
        type=str,
        default="data/bag-pkt/data.yaml",
        help="Path to data yaml file",
    )
    parser.add_argument(
        "--epochs", type=int, default=50, help="Number of epochs (default: 50)"
    )
    parser.add_argument(
        "--imgsz", type=int, default=640, help="Image size (default: 640)"
    )
    parser.add_argument(
        "--batch", type=int, default=16, help="Batch size (default: 16)"
    )
    parser.add_argument(
        "--project",
        type=str,
        default="tmp/runs",
        help="Project directory to save results (default: tmp/runs)",
    )
    return parser.parse_args()


def update_settings():
    """Update Ultralytics settings to use the current project directory."""
    settings.update(
        {
            "datasets_dir": "/app/data",
            "weights_dir": "/app/tmp/weights",
            "runs_dir": "/app/tmp/runs",
        }
    )


def main():
    args = parse_args()

    # update ultralytics settings
    update_settings()

    # Load YOLO model
    model = YOLO(args.model)

    project_path = Path(f"tmp/runs/{args.project}")

    project_path.mkdir(parents=True, exist_ok=True)

    # Train the model using the fertilizer bag dataset
    results = model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        patience=20,
        project=project_path,
    )

    # Save the trained model
    model.export(format="onnx")


if __name__ == "__main__":
    main()
