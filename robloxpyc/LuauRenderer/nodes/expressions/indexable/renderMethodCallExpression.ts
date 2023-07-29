import luau from "../../../../LuauAST";
import { assert } from "../../../../LuauAST/util/assert";
import { render, RenderState } from "../../../../LuauRenderer";
import { renderArguments } from "../../../../LuauRenderer/util/renderArguments";

export function renderMethodCallExpression(state: RenderState, node: luau.MethodCallExpression) {
	assert(luau.isValidIdentifier(node.name));
	return `${render(state, node.expression)}:${node.name}(${renderArguments(state, node.args)})`;
}
