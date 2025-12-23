import gymnasium as gym
from gymnasium.wrappers import RecordVideo
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.monitor import Monitor
import os

TOTAL_TIMESTEPS = 500_000 
MODEL_FOLDER = "models/lunar_lander_dqn"
VIDEO_FOLDER = "videos/lunar_lander"
LOG_FOLDER = "runs/lunar_lander_dqn"

os.makedirs(MODEL_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

train_env = gym.make("LunarLander-v3")
train_env = Monitor(train_env, LOG_FOLDER)

eval_env = gym.make("LunarLander-v3", render_mode="rgb_array")
eval_env = RecordVideo(
    eval_env,
    video_folder=VIDEO_FOLDER,
    episode_trigger=lambda ep: ep % 10 == 0,  # Record every 10th eval episode
    name_prefix="dqn_lunar"
)

eval_callback = EvalCallback(
    eval_env,
    best_model_save_path=MODEL_FOLDER,
    log_path=LOG_FOLDER,
    eval_freq=10_000,  # Evaluate every 10k steps
    n_eval_episodes=5,
    deterministic=True,
    render=False,
)

model = DQN(
    "MlpPolicy",
    train_env,
    learning_rate=1e-4,
    buffer_size=100_000,
    learning_starts=1_000,
    batch_size=64,
    gamma=0.99,
    exploration_fraction=0.1,
    exploration_final_eps=0.05,
    verbose=1,
    tensorboard_log=LOG_FOLDER,
)

print("Starting DQN training...")
print(f"Total timesteps: {TOTAL_TIMESTEPS:,}")
print("-" * 60)

model.learn(
    total_timesteps=TOTAL_TIMESTEPS,
    callback=eval_callback,
    progress_bar=True,
)

model.save(f"{MODEL_FOLDER}/dqn_lunar_final")
print(f"\nModel saved to {MODEL_FOLDER}/")

print("-" * 60)
print("Training complete!")
print(f"Best model saved to: {MODEL_FOLDER}/best_model.zip")
print(f"Videos saved to: {VIDEO_FOLDER}/")
print(f"Tensorboard logs: tensorboard --logdir {LOG_FOLDER}")

train_env.close()
eval_env.close()