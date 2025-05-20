import json

import wn

wn.download("omw:1.4")

# Initialize WordNets for each language
wordnets = {
  "en": "omw-en:1.4",
  "fr": "omw-fr:1.4",
  "es": "omw-es:1.4",
  "th": "omw-th:1.4",
  "zh": "omw-cmn:1.4",
}

wn_instances = {lang: wn.Wordnet(wordnets[lang]) for lang in wordnets}

# Top-level categories we know exist in all languages
TOP_LEVEL_CATEGORIES = [
  "animal",
  "plant",
  "vehicle",
  "furniture",
  "food",
  "clothing",
  "building",
  "tool",
  "weapon",
  "sport",
  "profession",
  "emotion",
  "color",
  "shape",
  "time",
  "weather",
  "body_part",
  "disease",
  "language",
]


def get_lemmas_for_language(synset, lang):
  """Get lemmas for a synset in a specific language, or empty list if not found."""
  if not synset.ili:
    return []
  lang_synset = wn_instances[lang].synsets(ili=synset.ili.id)
  if not lang_synset:
    return []
  return [lemma for lemma in lang_synset[0].lemmas()]


def build_tree_from_synset(synset, depth=0, max_depth=3):
  """Build a tree from a synset, including all hyponyms up to max_depth."""
  if depth > max_depth:
    return None

  # Get lemmas for each language
  lemmas = {}
  for lang in wordnets:
    lemmas[lang] = get_lemmas_for_language(synset, lang)

  # Get children (hyponyms)
  children = []
  for child in synset.hyponyms():
    subtree = build_tree_from_synset(child, depth + 1, max_depth)
    if subtree:
      children.append(subtree)

  return {"synset": synset.id, "lemmas": lemmas, "children": children}


def prune_tree(tree):
  """Remove nodes that don't have lemmas in all languages."""
  if not tree:
    return None

  # Check if this node has lemmas in all languages
  has_full_coverage = all(len(lemmas) > 0 for lemmas in tree["lemmas"].values())
  if not has_full_coverage:
    return None

  # Recursively prune children
  pruned_children = []
  for child in tree["children"]:
    pruned_child = prune_tree(child)
    if pruned_child:
      pruned_children.append(pruned_child)

  # Only keep this node if it has children or is a leaf
  if pruned_children or not tree["children"]:
    return {"synset": tree["synset"], "lemmas": tree["lemmas"], "children": pruned_children}
  return None


def build_forest():
  """Build a forest starting from known top-level categories."""
  forest = []

  for category in TOP_LEVEL_CATEGORIES:
    print(f"Processing category: {category}")
    # Get English synset
    en_synsets = wn_instances["en"].synsets(category, pos="n")
    if not en_synsets:
      print(f"  No English synset found for {category}")
      continue

    # Use the first synset
    root_synset = en_synsets[0]
    tree = build_tree_from_synset(root_synset, max_depth=3)
    if tree:
      # Prune the tree to only keep nodes with full coverage
      pruned_tree = prune_tree(tree)
      if pruned_tree:
        forest.append(pruned_tree)
        print(f"  Added tree with {len(pruned_tree['children'])} children")
      else:
        print(f"  Tree pruned to empty for {category}")
    else:
      print(f"  No tree built for {category}")

  return forest


if __name__ == "__main__":
  print("Building forest from top-level categories...")
  forest = build_forest()

  print(f"Built forest with {len(forest)} categories")
  path = "wordnet_dataset.json"
  with open(path, "w") as f:
    json.dump(forest, f, indent=2, ensure_ascii=False)
  print(f"Forest saved to {path}")
