import luau from "../../../../LuauAST";
import { assert } from "../../../../LuauAST/util/assert";
import { RenderState } from "../../../../LuauRenderer";

export function renderTemporaryIdentifier(state: RenderState, node: luau.TemporaryIdentifier) {
	const name = state.getTempName(node);
	assert(luau.isValidIdentifier(name), `Invalid Temporary Identifier: "${name}"`);
	return name;
}
