const {StandardMerkleTree} = require("@openzeppelin/merkle-tree")
const fs = require("fs")
// (1)
const values = [
  ["0x3941e7bee4DA080C6f8809c09bD2bc2Cc393feE0", "1", "123000000"],
  ["0xB783ea74D78d295945AdE6f2e45f3cB0b467EbaC", "1", "456000000"],
  ["0x4B5eA043679d62F0199DA3Fc7731b6dCDc775C35", "1", "789000000"],
  ["0x50c6b2F2407f971913341ADEDc843d620E30baAa", "1", "101112000000"],
  ["0x5ADD71300d924213456b037b5be25020C62D9e08", "1", "131415000000"],
  ["0xc8f32157826C09a094b4F0A3C7fa0bA5321866ae", "1", "161718000000"],
  ["0x15f8F85c0B22cc5614E7eb353fA69AedC166d579", "1", "192021000000"],
  ["0x9834B51f25E0f94058537cD4Ffa8E79e7D9c54cc", "1", "222324000000"],
  ["0xe8dfb173f605cf1dd8d13d21978df0d599b3d081", "1", "252627000000"],
];

//total 1062585000000

// (2)
const tree = StandardMerkleTree.of(values, ["address", "uint256", "uint256"]);

// (3)
console.log('Merkle Root:', tree.root);

// (4)
fs.writeFileSync("tree.json", JSON.stringify(tree.dump()));