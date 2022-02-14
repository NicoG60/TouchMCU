local data = {}

-- Using the touch as value for the CC is a trick
-- Without it, MIDI messages never get routed.

-- this sctipt uses bit_utils and led_utils

function init()
  for i = start, stop do
    data[(i-start)+1] = 0x20
  end
end

function onReceiveMIDI(message, connections)
  local status, data1, data2 = table.unpack(message)

  -- status should be dealt with by the MIDI routing, let's trust that

  data[(data1-start)+1] = data2

  local str = ''
  for i = start, stop do
    local d = data[(i-start)+1]
    local pt = false

    if isBitSet(d, 6) then
      pt = true
      d = clearBit(d, 6)
    end

    if d < 0x20 then
      d = d + 2^6
    end

    if pt == true then
      str = string.char(d) .. '.' .. str
    else
      str = string.char(d) .. str
    end
  end

  self.values.text = str
end  