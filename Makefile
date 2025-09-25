# FixPipeline - Professional Build System

.PHONY: install clean build-deb test

# Install dependencies for building
install-deps:
	pip install stdeb

# Build .deb package
build-deb: install-deps
	python setup.py --command-packages=stdeb.command bdist_deb
	@echo "✅ .deb package created in deb_dist/"

# Clean build artifacts
clean:
	rm -rf build/ dist/ *.egg-info/ deb_dist/ .venv/

# Test installation
test:
	python -m venv .venv
	.venv/bin/pip install -e .
	.venv/bin/fixpipeline --version

# Create release package
release: clean build-deb
	@echo "📦 Release package ready in deb_dist/"
