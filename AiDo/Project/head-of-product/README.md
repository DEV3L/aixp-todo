# AiDo - Virtual Head of Product - Alex Parker

Meet Alex Parker, your AI-powered Head of Product. Alex excels in product management, agile methodologies, and AI technologies. Get strategic insights, manage product backlogs, and refine user stories seamlessly. Access Alex for expert guidance on product development and optimization.

[Assistants API Beta](https://platform.openai.com/docs/assistants/overview)

## Setup

1. Copy the env.local file to a new file named .env and replace `OPENAI_API_KEY` with your actual OpenAI API key:

```bash
cp env.local .env
```

3. Setup a virtual environment with dependencies and activate it:

```bash
brew install hatch
hatch env create
hatch shell
```

1. Run the main script:

```bash
python run_chat.py
```

## Testing

### Unit Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov
```

With coverage for Coverage Gutters:

```bash
pytest --cov --cov-report lcov

Command + Shift + P => Coverage Gutters: Watch
```

## Contributing

We welcome contributions!

## License

This project is licensed under the Beer-Ware License - see the [LICENSE](LICENSE) file for details.
