# 🤝 Contributing to Pi-5 Relay Controller

Thank you for your interest in contributing to Pi-5 Relay Controller! We welcome contributions from the community and are excited to see what you'll bring to the project.

## 🌟 Ways to Contribute

- 🐛 **Bug Reports**: Found a bug? Let us know!
- 💡 **Feature Requests**: Have an idea? We'd love to hear it!
- 📝 **Documentation**: Help improve our docs
- 🔧 **Code Contributions**: Submit pull requests
- 🌍 **Translations**: Help us support more languages
- 🧪 **Testing**: Test on different hardware configurations

## 🚀 Getting Started

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/Pi-5-Relay-Controller.git
   cd Pi-5-Relay-Controller
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run in development mode**
   ```bash
   python3 server.py
   ```

### Development Guidelines

- **Code Style**: Follow PEP 8 for Python code
- **Comments**: Write clear, concise comments
- **Testing**: Test your changes thoroughly
- **Documentation**: Update docs for new features

## 📝 Submitting Changes

### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes**
   - Write clean, well-documented code
   - Follow existing code style
   - Add tests if applicable

3. **Test your changes**
   ```bash
   # Test the web interface
   # Test GPIO functionality (if available)
   # Test service installation
   ```

4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Create a Pull Request**
   - Use a clear, descriptive title
   - Describe what your changes do
   - Reference any related issues

### Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when applicable

Examples:
```
Add support for 32-channel relay modules
Fix GPIO initialization on Pi 5
Update documentation for new API endpoints
```

## 🐛 Bug Reports

When reporting bugs, please include:

- **Environment**: Raspberry Pi model, OS version, Python version
- **Steps to reproduce**: Clear, step-by-step instructions
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Screenshots**: If applicable
- **Logs**: Relevant error messages or logs

## 💡 Feature Requests

When suggesting features:

- **Use case**: Describe why this feature would be useful
- **Implementation**: If you have ideas on how to implement it
- **Alternatives**: Any alternative solutions you've considered
- **Additional context**: Screenshots, mockups, or examples

## 🧪 Testing

### Manual Testing Checklist

- [ ] Web interface loads correctly
- [ ] Login/logout functionality works
- [ ] All relay controls respond properly
- [ ] State persistence works after reboot
- [ ] Service starts/stops correctly
- [ ] Mobile interface is responsive

### Hardware Testing

If you have access to relay hardware:

- [ ] GPIO pins control relays correctly
- [ ] All 16 channels work independently
- [ ] No GPIO conflicts with other services
- [ ] Proper electrical isolation

## 📚 Documentation

Help us improve documentation:

- **README**: Keep installation and usage instructions clear
- **Code Comments**: Explain complex logic
- **API Documentation**: Document all endpoints
- **Examples**: Provide usage examples

## 🌍 Internationalization

We welcome translations! Currently supported:

- English (en)
- Arabic (ar)

To add a new language:

1. Create translation files for templates
2. Update CSS for RTL/LTR support
3. Test the interface thoroughly

## 🏷️ Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Create release notes
4. Tag the release
5. Update documentation

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: For security issues or private matters

## 🙏 Recognition

Contributors will be:

- Listed in the README
- Mentioned in release notes
- Given credit in commit messages

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Pi-5 Relay Controller! 🎉
