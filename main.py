import hydra

from omegaconf import DictConfig

from pywasn.client import client


@hydra.main(config_path="config", config_name="config")
def main(config: DictConfig):
    client(config)


if __name__ == "__main__":
    main()
