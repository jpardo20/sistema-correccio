from motor.repo_locator import RepoLocator

locator = RepoLocator()

print("Unitats detectades:")
print(locator.get_units())

print("\nRepositoris:")
locator.debug_print()

for u in locator.get_units():
    print(u, locator.repo_exists(u))