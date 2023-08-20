import luau from "../../../LuauAST";
import { render, RenderState } from "../../../LuauRenderer";
import { renderStatements } from "../../../LuauRenderer/util/renderStatements";

export function renderNumericForStatement(state: RenderState, node: luau.NumericForStatement) {
	const idStr = render(state, node.id);
	const startStr = render(state, node.start);
	const endStr = render(state, node.end);

	let predicateStr = `${startStr}, ${endStr}`;

	// step of 1 can be omitted
	if (node.step && (!luau.isNumberLiteral(node.step) || Number(node.step.value) !== 1)) {
		const stepStr = render(state, node.step);
		predicateStr += `, ${stepStr}`;
	}

	let result = "";
	result += state.line(`for ${idStr} = ${predicateStr} do`);
	result += state.block(() => renderStatements(state, node.statements));
	result += state.line(`end`);

	return result;
}
