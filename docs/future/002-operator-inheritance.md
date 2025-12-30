# Decision: Operator Inheritance System

**Date**: 2025-08-02  
**Status**: Implemented ✅  
**Impact**: High - Enables configuration composition

## Problem

How should users customize shell configurations without:

- Duplicating common settings
- Forking the entire project
- Losing upstream improvements
- Creating merge conflicts

Initial idea was to have separate operators for each personality, but this led to duplication.

## Options Considered

### Option 1: Flat Operators (No Inheritance)

```text
operators/
├── base/
├── jiveturkey/      # Full config duplication
├── matrix/          # Full config duplication
└── minimalist/      # Full config duplication
```

**Pros**: Simple, clear
**Cons**: Massive duplication, hard to maintain

### Option 2: Mixin System

```yaml
# Complex mixin composition
mixins: [ "base", "matrix-theme", "power-user", "git-shortcuts" ]
```

**Pros**: Very flexible
**Cons**: Complex dependency resolution, order matters

### Option 3: Single Inheritance + Themes ✅

```yaml
# jiveturkey operator
extends: "base"
theme: "matrix"
```

**Pros**: Simple inheritance, clear hierarchy, theme composition
**Cons**: Limited to single inheritance

## Decision

**Chosen**: Single inheritance with theme support

### Inheritance Chain

```text
base → jiveturkey (base + matrix theme + power-user features)
base → matrix (base + pure matrix aesthetics)
base → minimalist (base - extras)
```

### Theme System

Themes are special operators that provide:

- Visual styling (prompts, colors)
- Thematic commands (Matrix: `redpill`, `bluepill`)
- Aesthetic aliases (`hack`, `enter_matrix`)

## Implementation

### OperatorManager Resolution

```python
def load_operator(self, operator_name: str, module_type: str):
  config = self._load_config(operator_name, module_type)

  # Handle inheritance
  if 'extends' in config:
    parent = self.load_operator(config['extends'], module_type)
    config = self._merge_configs(parent, config)

  # Apply theme
  if 'theme' in config:
    theme = self.load_operator(config['theme'], module_type)
    config = self._apply_theme(config, theme)

  return config
```

### Merge Strategy: Last Wins

```python
def _merge_configs(self, parent: Dict, child: Dict) -> Dict:
  merged = parent.copy()
  for key, value in child.items():
    if key == 'files':
      merged.setdefault('files', {}).update(value)
    else:
      merged[key] = value  # Child wins conflicts
  return merged
```

## Real-World Example

### Base Operator

```yaml
# operators/base/shell/operator.yaml
name: "base-shell"
features: [ "basic-aliases", "git-shortcuts" ]
files: [ "zshrc", "bashrc" ]
```

### JiveTurkey Operator

```yaml
# operators/jiveturkey/shell/operator.yaml
name: "jiveturkey-shell"
extends: "base"
theme: "matrix"
features: [ "productivity-aliases", "docker-mastery", "kubernetes-ninja" ]
files: [ "zshrc" ]
```

### Result

JiveTurkey gets:

- Basic aliases from `base`
- Git shortcuts from `base`
- Matrix theme from `matrix`
- Power-user features from `jiveturkey`
- All combined in final zshrc

## Benefits Realized

1. **DRY Principle**: No configuration duplication
2. **Upstream Benefits**: Base improvements flow to all operators
3. **Theme Reusability**: Matrix theme can be used by any operator
4. **Clear Hierarchy**: Easy to understand inheritance chain
5. **Conflict Resolution**: Last-wins is predictable

## User Experience

### Before (Flat Structure)

```bash
# User wants Matrix theme + personal preferences
# Must choose: matrix OR jiveturkey, can't combine
neosetup shell --operator matrix    # Gets theme, loses preferences
neosetup shell --operator jiveturkey # Gets preferences, loses theme
```

### After (Inheritance)

```bash
# User gets Matrix theme AND personal preferences
neosetup shell --operator jiveturkey  # Gets base + matrix + personal
```

## Edge Cases Handled

### Circular Dependencies

```python
def _detect_cycles(self, operator_name: str, visited: Set[str]):
  if operator_name in visited:
    raise ValueError(f"Circular dependency: {visited} -> {operator_name}")
```

### Missing Parents

```python
def load_operator(self, operator_name: str, module_type: str):
  if not self.operator_exists(operator_name, module_type):
    if operator_name == "base":
      self._create_base_operator()  # Auto-create base
    else:
      return None  # Graceful degradation
```

### Theme Conflicts

Theme commands override base commands, allowing Matrix aesthetic to take precedence over generic commands.

## Future Enhancements

### Multiple Inheritance (Considered)

```yaml
# Future possibility
extends: [ "base", "power-user" ]  
```

**Pros**: More flexibility  
**Cons**: Diamond problem, complexity

### Theme Stacking

```yaml
# Future possibility  
themes: [ "matrix", "cyberpunk", "neon" ]
```

### Operator Versioning

```yaml
# Future possibility
extends: "base@1.2.0"
theme: "matrix@latest"
```

## Success Metrics

✅ **Code Reuse**: Base operator used by 3/4 operators  
✅ **Theme Reuse**: Matrix theme could be used by any operator  
✅ **Maintainability**: Base changes propagate automatically  
✅ **User Satisfaction**: JiveTurkey gets personal + theme preferences  
✅ **Simplicity**: Single inheritance is easy to understand

## Lessons Learned

1. **Single inheritance is sufficient** - Multiple inheritance adds complexity without clear benefit
2. **Themes are special operators** - Treating themes as operators maintains consistency
3. **Last-wins merge is predictable** - Users understand that child overrides parent
4. **Auto-creation of base is helpful** - Reduces setup friction

This inheritance system enables powerful configuration composition while maintaining simplicity and predictability.
