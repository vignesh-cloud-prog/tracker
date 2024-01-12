# Video Tracker

Video Tracker is a simple yet powerful application designed to help you track your progress in multiple video courses. Easily manage watched and completed videos within an intuitive interface.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Launching the Application](#launching-the-application)
  - [Managing Courses and Videos](#managing-courses-and-videos)
- [Development](#development)
  - [Building the Executable](#building-the-executable)
  - [Making Changes](#making-changes)
  - [Pushing Changes](#pushing-changes)
- [Contributing](#contributing)
- [License](#license)

## Features

- Track progress in multiple video courses.
- Mark videos as watched or completed.
- User-friendly interface for easy navigation.
- Support for managing multiple folders.

## Getting Started

### Prerequisites

- Python 3.x
- Tkinter library

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/vignesh-cloud-prog/tracker.git
   cd videotracker
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Launching the Application

Run the following command to launch Video Tracker:

```bash
python tracker.py
```

### Managing Courses and Videos

- Open the application.
- Navigate through courses and folders.
- Mark videos as watched or completed.

## Development

### Building the Executable

To create an executable file for distribution, you can use tools like `pyinstaller` or `cx_Freeze`. For example, using `pyinstaller`:

```bash
pyinstaller --onefile tracker.py
```

This will generate a standalone executable in the `dist` directory.

### Making Changes

1. Create a new branch for your changes:

   ```bash
   git checkout -b feature/new-feature
   ```

2. Make your changes and commit them:

   ```bash
   git add .
   git commit -m "Add new feature"
   ```

### Pushing Changes

Push your changes to the remote repository:

```bash
git push origin feature/new-feature
```

Submit a pull request on GitHub for review and merge.

## Contributing

Contributions are welcome! Please follow the [Contributing Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).
