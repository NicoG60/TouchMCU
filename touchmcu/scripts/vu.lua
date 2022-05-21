-- Using the touch as value for the CP is a trick
-- Without it, MIDI messages never get routed.

-- this sctipt uses led_utils

function onReceiveMIDI(message, connections)
  local status, data1 = table.unpack(message)

  -- we don't care about status and data1, these should be
  -- alright because of the MIDI routing.
  -- let's just process the value in data2
  
  -- some byte manipulation here,
  -- - the 4 msb are the track number
  -- - the 4 lsb are the value
  local rtrack = math.floor(data1 / 16)
  
  -- Not me, skip
  if rtrack ~= track then
    return
  end
  
  local value = data1 - (rtrack * 16)
  
  for i = 1, 11, 1 do
    local led = findLed(i)
    if value >= i then
      led.values.x = 1
    else
      led.values.x = 0
    end
  end
end