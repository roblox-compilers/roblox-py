import luau from "../../LuauAST";

// base types
export interface BaseNode<T extends luau.SyntaxKind = luau.SyntaxKind> {
	kind: T;
	parent?: luau.Node;
}

export interface BaseIndexableExpression<
	T extends keyof luau.IndexableExpressionByKind = keyof luau.IndexableExpressionByKind,
> extends luau.BaseNode<T> {}

export interface BaseExpression<T extends keyof luau.ExpressionByKind = keyof luau.ExpressionByKind>
	extends luau.BaseNode<T> {}

export interface BaseStatement<T extends keyof luau.StatementByKind = keyof luau.StatementByKind>
	extends luau.BaseNode<T> {}

export interface BaseField<T extends keyof luau.FieldByKind = keyof luau.FieldByKind> extends luau.BaseNode<T> {}

export interface HasParameters {
	parameters: luau.List<luau.AnyIdentifier>;
	hasDotDotDot: boolean;
}

export type AnyIdentifier = luau.Identifier | luau.TemporaryIdentifier;

export type WritableExpression = luau.AnyIdentifier | luau.PropertyAccessExpression | luau.ComputedIndexExpression;

export type SimpleTypes =
	| luau.Identifier
	| luau.TemporaryIdentifier
	| luau.NilLiteral
	| luau.TrueLiteral
	| luau.FalseLiteral
	| luau.NumberLiteral
	| luau.StringLiteral;

export type ExpressionWithPrecedence = luau.IfExpression | luau.UnaryExpression | luau.BinaryExpression;

// expressions
export interface None extends luau.BaseExpression<luau.SyntaxKind.None> {}

export interface NilLiteral extends luau.BaseExpression<luau.SyntaxKind.NilLiteral> {}

export interface FalseLiteral extends luau.BaseExpression<luau.SyntaxKind.FalseLiteral> {}

export interface TrueLiteral extends luau.BaseExpression<luau.SyntaxKind.TrueLiteral> {}

export interface NumberLiteral extends luau.BaseExpression<luau.SyntaxKind.NumberLiteral> {
	value: string;
}

export interface StringLiteral extends luau.BaseExpression<luau.SyntaxKind.StringLiteral> {
	value: string;
}

export interface VarArgsLiteral extends luau.BaseExpression<luau.SyntaxKind.VarArgsLiteral> {}

export interface FunctionExpression extends luau.BaseExpression<luau.SyntaxKind.FunctionExpression>, HasParameters {
	statements: luau.List<luau.Statement>;
}

export interface Identifier extends luau.BaseExpression<luau.SyntaxKind.Identifier> {
	name: string;
}

export interface TemporaryIdentifier extends luau.BaseExpression<luau.SyntaxKind.TemporaryIdentifier> {
	name: string;
	id: number;
}

export interface ComputedIndexExpression extends luau.BaseExpression<luau.SyntaxKind.ComputedIndexExpression> {
	expression: luau.IndexableExpression;
	index: luau.Expression;
}

export interface PropertyAccessExpression extends luau.BaseExpression<luau.SyntaxKind.PropertyAccessExpression> {
	expression: luau.IndexableExpression;
	name: string;
}

export interface CallExpression extends luau.BaseExpression<luau.SyntaxKind.CallExpression> {
	expression: luau.IndexableExpression;
	args: luau.List<luau.Expression>;
}

export interface MethodCallExpression extends luau.BaseExpression<luau.SyntaxKind.MethodCallExpression> {
	name: string;
	expression: luau.IndexableExpression;
	args: luau.List<luau.Expression>;
}

export interface ParenthesizedExpression extends luau.BaseExpression<luau.SyntaxKind.ParenthesizedExpression> {
	expression: luau.Expression;
}

export interface BinaryExpression extends luau.BaseExpression<luau.SyntaxKind.BinaryExpression> {
	left: luau.Expression;
	operator: luau.BinaryOperator;
	right: luau.Expression;
}

export interface UnaryExpression extends luau.BaseExpression<luau.SyntaxKind.UnaryExpression> {
	operator: luau.UnaryOperator;
	expression: luau.Expression;
}

export interface IfExpression extends luau.BaseExpression<luau.SyntaxKind.IfExpression> {
	condition: luau.Expression;
	expression: luau.Expression;
	alternative: luau.Expression;
}

export interface Array extends luau.BaseExpression<luau.SyntaxKind.Array> {
	members: luau.List<luau.Expression>;
}

export interface Map extends luau.BaseExpression<luau.SyntaxKind.Map> {
	fields: luau.List<luau.MapField>;
}

export interface Set extends luau.BaseExpression<luau.SyntaxKind.Set> {
	members: luau.List<luau.Expression>;
}

export interface MixedTable extends luau.BaseExpression<luau.SyntaxKind.MixedTable> {
	fields: luau.List<luau.MapField | luau.Expression>;
}

// statements
export interface Assignment extends luau.BaseStatement<luau.SyntaxKind.Assignment> {
	left: luau.WritableExpression | luau.List<luau.WritableExpression>;
	operator: luau.AssignmentOperator;
	right: luau.Expression | luau.List<luau.Expression>;
}

export interface BreakStatement extends luau.BaseStatement<luau.SyntaxKind.BreakStatement> {}

export interface CallStatement extends luau.BaseStatement<luau.SyntaxKind.CallStatement> {
	expression: luau.CallExpression | luau.MethodCallExpression;
}

export interface ContinueStatement extends luau.BaseStatement<luau.SyntaxKind.ContinueStatement> {}

export interface DoStatement extends luau.BaseStatement<luau.SyntaxKind.DoStatement> {
	statements: luau.List<luau.Statement>;
}

export interface WhileStatement extends luau.BaseStatement<luau.SyntaxKind.WhileStatement> {
	condition: luau.Expression;
	statements: luau.List<luau.Statement>;
}

export interface RepeatStatement extends luau.BaseStatement<luau.SyntaxKind.RepeatStatement> {
	condition: luau.Expression;
	statements: luau.List<luau.Statement>;
}

export interface IfStatement extends luau.BaseStatement<luau.SyntaxKind.IfStatement> {
	condition: luau.Expression;
	statements: luau.List<luau.Statement>;
	elseBody: luau.IfStatement | luau.List<luau.Statement>;
}

export interface NumericForStatement extends luau.BaseStatement<luau.SyntaxKind.NumericForStatement> {
	id: luau.AnyIdentifier;
	start: luau.Expression;
	end: luau.Expression;
	step?: luau.Expression;
	statements: luau.List<luau.Statement>;
}

export interface ForStatement extends luau.BaseStatement<luau.SyntaxKind.ForStatement> {
	ids: luau.List<luau.AnyIdentifier>;
	expression: luau.Expression;
	statements: luau.List<luau.Statement>;
}

export interface FunctionDeclaration extends luau.BaseStatement<luau.SyntaxKind.FunctionDeclaration>, HasParameters {
	localize: boolean;
	name: luau.AnyIdentifier | luau.PropertyAccessExpression;
	statements: luau.List<luau.Statement>;
}

export interface MethodDeclaration extends luau.BaseStatement<luau.SyntaxKind.MethodDeclaration>, HasParameters {
	expression: luau.IndexableExpression;
	name: string;
	statements: luau.List<luau.Statement>;
}

export interface VariableDeclaration extends luau.BaseStatement<luau.SyntaxKind.VariableDeclaration> {
	left: luau.AnyIdentifier | luau.List<luau.AnyIdentifier>;
	right: luau.Expression | luau.List<luau.Expression> | undefined;
}

export interface ReturnStatement extends luau.BaseStatement<luau.SyntaxKind.ReturnStatement> {
	expression: luau.Expression | luau.List<luau.Expression>;
}

export interface Comment extends luau.BaseStatement<luau.SyntaxKind.Comment> {
	text: string;
}

// fields
export interface MapField extends luau.BaseField<luau.SyntaxKind.MapField> {
	index: luau.Expression;
	value: luau.Expression;
}
