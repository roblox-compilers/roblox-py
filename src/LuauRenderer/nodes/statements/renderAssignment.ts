import luau from "../../../LuauAST";
import { assert } from "../../../LuauAST/util/assert";
import { render, RenderState } from "../../../LuauRenderer";

export function renderAssignment(state: RenderState, node: luau.Assignment) {
	let leftStr: string;
	if (luau.list.isList(node.left)) {
		assert(!luau.list.isEmpty(node.left));
		leftStr = luau.list.mapToArray(node.left, id => render(state, id)).join(", ");
	} else {
		leftStr = render(state, node.left);
	}

	let rightStr: string;
	if (luau.list.isList(node.right)) {
		assert(!luau.list.isEmpty(node.right));
		rightStr = luau.list.mapToArray(node.right, expression => render(state, expression)).join(", ");
	} else {
		rightStr = render(state, node.right);
	}

	return state.line(`${leftStr} ${node.operator} ${rightStr}`, node);
}
