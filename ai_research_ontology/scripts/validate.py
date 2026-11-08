"""Validate the proposed ontology, public literature and synthetic internal graph."""
import sys
from ontology import load_bundle, validate


def main():
    try:
        bundle = load_bundle()
        errors = validate(bundle)
    except (ValueError, KeyError, TypeError) as error:
        print(f"INVALID: {error}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1
    print(f"VALID: {len(bundle.entities)} entities, {len(bundle.schema['classes'])} types; snapshot as_of={bundle.as_of}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
