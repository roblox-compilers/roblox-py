local Toolbar = plugin:CreateToolbar("Roblox.py")
local PythonButton = Toolbar:CreateButton("Python IDE", "Open the python editor/compiler", "rbxassetid://5937429524", "Python")
PythonButton.Click:Connect(function()
	local PythonWidgetInfo = DockWidgetPluginGuiInfo.new(
		Enum.InitialDockState.Float,
		false,   -- Widget will be initially enabled
		false,  -- Don't override the previous enabled state
		200,    -- Default width of the floating window
		300,    -- Default height of the floating window
		150,    -- Minimum width of the floating window (optional)
		150     -- Minimum height of the floating window (optional)
	)

	local PythonWidget = plugin:CreateDockWidgetPluginGui("Python", PythonWidgetInfo)
	PythonWidget.Title = "Python Script Editor"
	local PythonGui = script.Parent.Main
	PythonGui.Parent = PythonWidget
	
	local Highlighter = require(script.Highlighter)
	local TextBoxPlus = require(script.TextBoxPlus)
	local Lang = require(script.Highlighter.lexer.language)
	
	local TB = TextBoxPlus.new(
		PythonGui.TextBoxBackground,
		{
			TextSize = 15;
			TextWrapped = false;
			Font = Enum.Font.Code;
			MultiLine = true;
			TextColor3 = Color3.new(1,1,1)
		}
	)
	


	local last = tick()

	local instance
	local internal

	local autofill = PythonGui:FindFirstChild("Autofill")

	PythonWidget.Enabled = true

	instance = game.Selection:Get()[1]

	if (not instance) or (not instance:IsA("BaseScript")) then
		instance = Instance.new("Script",game.Selection:Get()[1] or workspace)
		instance.Name = "Script.py"

		instance:SetAttribute("Source", "")
		internal = ""
		PythonGui:WaitForChild("TextBoxBackground").TextPlus.Input.Text  = ""
	elseif not (instance.Name:split(".")[#instance.Name:split(".")] == "py") then
		PythonWidget.Enabled = false
		error("The selected script is not a .py script.")
	else 
		internal = instance:GetAttribute("Source")
		PythonGui:WaitForChild("TextBoxBackground").TextPlus.Input.Text = internal or ""
	end

	if not game.ReplicatedStorage:FindFirstChild("Roblox.py") then
		script["Roblox.py"]:Clone().Parent = game.ReplicatedStorage
	end

	PythonWidget.Title = instance.Name
	

	local function debugfunc()
		local code = PythonGui.TextBoxBackground.TextPlus.Input.Text
		local url = "https://python-lua--aaravsethi4.repl.co/debug"
		local http = game.HttpService
		local response
		pcall(function()
			response = http:PostAsync(url, code)
		end)

		if response and response ~= "" and response ~= " " and response ~= "****" then 
			response = response:gsub("************* Module debug", "")
			local line = response:sub(9):sub(1,4)
			print(line)
		end
	end
	local function get()
		if not PythonGui.TextBoxBackground:FindFirstChild("TextPlus") then return end
		local code = PythonGui.TextBoxBackground.TextPlus.Input.Text
		last = tick()
		local url = "https://python-lua--aaravsethi4.repl.co"

		local http = game.HttpService
		PythonGui.TextButton.BackgroundColor3 = Color3.fromRGB(251, 217, 94)
		local response
		pcall(function()
			response = http:PostAsync(url, code)
		end)
		if response then
			if response:sub(1,#("CompileError!:")) == "CompileError!:" then
				PythonGui.TextButton.BackgroundColor3 = Color3.fromRGB(252, 76, 84)
				task.wait(3)
				PythonGui.TextButton.BackgroundColor3 = Color3.fromRGB(93, 255, 141)
				error("Roblox.py | Compilation Error: \n"..response:sub(#("CompileError!:")))
				return response
			end

			PythonGui.TextButton.BackgroundColor3 = Color3.fromRGB(93, 255, 141)
			internal = code
			instance:SetAttribute("Source", code)
			instance.Source = [[--// Compiled using Roblox.py \\--
		
		
------------------------------------ BUILT IN -------------------------------
local class, range, __name__, len = unpack(require(game.ReplicatedStorage["Roblox.py"])(script))
-----------------------------------------------------------------------------
]]..response
			return response
		else
			PythonGui.TextButton.BackgroundColor3 = Color3.fromRGB(252, 76, 84)
			task.wait(3)
			PythonGui.TextButton.BackgroundColor3 = Color3.fromRGB(93, 255, 141)
			return ""
		end
	end

	function autofill(items, leng)
		PythonGui:FindFirstChild("Autofill").Visible = true

		-- duplicate
		for i, v in items do
			if PythonGui.Autofill.Items:GetChildren()[i]:IsA("TextButton") then
				local clone = PythonGui.Autofill.Items:GetChildren()[i]
				clone.Parent =  PythonGui:FindFirstChild("Autofill").Items
				clone.Name = v
				clone.Text = v

				clone.MouseButton1Click:Connect(function()
					local before = PythonGui.TextBoxBackground.TextPlus.Input.Text:sub(1,PythonGui.TextBoxBackground.TextPlus.Input.CursorPosition)
					local after = PythonGui.TextBoxBackground.TextPlus.Input.Text:sub(PythonGui.TextBoxBackground.TextPlus.Input.CursorPosition)

					local complete = v:sub(leng)

					PythonGui.TextBoxBackground.TextPlus.Input.Text = before..complete..after
				end)
			end
		end	
	end

	local function getAutofillresults(line)
		local all = {}
		local lib = {}
		local set 
		local nonsplit = "abcdefghijklmnopqrstuvwxyz1234567890"
		nonsplit = nonsplit:split("")

		for i, v in Lang do
			for ii, vv in v do
				if typeof(vv) == "table" then lib[ii] = vv end
				table.insert(all, ii)
			end
		end
		-----------------
		local wordStartPos = 0
		for i, v in line:split("") do
			if not table.find(nonsplit, v) then
				-- this is a split
				wordStartPos = i
			elseif v == "." then
				if lib[line:sub(wordStartPos+1)] then
					-- show reccomendations ONLY of the library
					set = lib[line:sub(wordStartPos+1)]
					wordStartPos = i
				end 
			end
		end
		local word = line:sub(wordStartPos+1)
		-----------------
		local valid = {}
		if not set then
			for i, v in all do
				if v:sub(1, #word) == word then
					table.insert(valid, v)
				end
			end
		else
			for i, v in set do
				if i:sub(1, #word) == word then
					table.insert(valid, i)
				end
			end
		end

		autofill(valid, #line-wordStartPos)
	end

	local real = PythonGui.TextBoxBackground.TextPlus.Input
	Highlighter.highlight({
		textObject = real,
	})
	real.Changed:Connect(function()
		local lines = real.Text:split("\n")
		local text = ""
		local pos = real.CursorPosition

		local before = string.sub(real.Text,1, pos-1)
		local newlines = before:split("\n")

		for i = 1, #lines do
			if i == #newlines then
				text = text.."<b>"..i.."</b>\n"
			else 
				text = text..i.."\n"
			end
		end
		pcall(function()
			PythonGui.NumberLine.CanvasSize = UDim2.new(0,0, PythonGui:WaitForChild("TextBoxBackground").TextPlus.CanvasSize.Y.Scale, PythonGui.TextBoxBackground.TextPlus.CanvasSize.Y.Offset)
			PythonGui.NumberLine.CanvasPosition = Vector2.new(0, PythonGui.TextBoxBackground.TextPlus.CanvasPosition.Y)
			if PythonGui.NumberLine.TextLabel.Text ~= text then
				PythonGui.NumberLine.TextLabel.Text = text
			end
		end)
		TB.HistoryController:TakeSnapshot()
		--getAutofillresults(lines[#newlines])
	end)
	PythonGui.TextButton.MouseButton1Click:Connect(function()
		get()
	end)
	coroutine.wrap(function()
		while tick()-last>10 do
			get()
		end
	end)()
	while task.wait(1) do
		--debugfunc()
	end
end)
