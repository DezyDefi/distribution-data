const {StandardMerkleTree} = require("@openzeppelin/merkle-tree")
const fs = require("fs")

// (1)
const tree = StandardMerkleTree.load(JSON.parse(fs.readFileSync("tree.json")));

// (2)
for (const [i, v] of tree.entries()) {
  if (v[0] === '0x15f8F85c0B22cc5614E7eb353fA69AedC166d579') {
    // (3)
    const proof = tree.getProof(i);
    console.log('root:',tree.root)
    console.log('Value:', v);
    console.log('Proof:', proof);
  }
}