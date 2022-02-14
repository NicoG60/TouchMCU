local lcds = {}
local content = string.rep(" ", 56*2)

function init()
  lcds = self:findAllByName("lcd", true)
end

function onReceiveMIDI(message, connections)

  -- Check sysex Header
  local header = table.pack(table.unpack(message, 1, 6))
  if not compareTables(header, {0xF0, 0x00, 0x00, 0x66, 0x14, 0x12}) then
    return -- Wrong sysex header, skipping
  end

  -- Extract information
  local start = message[7] + 1
  local str = string.char(table.unpack(message, 8, #message-1))

  -- Replace in our local string
  content = string.sub(content, 1, start-1) .. str .. string.sub(content, start+#str)

  -- Send out to the different LCDs
  for i = 0, 7 do
    local i1 = i+1

    local s1 = (7*i)+1
    local s2 = s1+56

    local l1 = string.sub(content, s1, s1+6)
    local l2 = string.sub(content, s2, s2+6)

    local str = l1.."\n"..l2

    lcds[i1].values.text = str
  end
end