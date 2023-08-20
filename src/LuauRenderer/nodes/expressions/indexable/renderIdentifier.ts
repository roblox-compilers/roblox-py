import luau from "../../../../LuauAST";
import { assert } from "../../../../LuauAST/util/assert";
import { RenderState } from "../../../../LuauRenderer";

export function renderIdentifier(state: RenderState, node: luau.Identifier) {
	assert(luau.isValidIdentifier(node.name), `Invalid Luau Identifier: "${node.name}"`);
	return node.name;
}
