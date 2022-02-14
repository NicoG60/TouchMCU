-- Using the touch as value for the CC is a trick
-- Without it, MIDI messages never get routed.

-- this sctipt uses bit_utils and led_utils

function onReceiveMIDI(message, connections)
  local status, data1, data2 = table.unpack(message)

  -- we don't care about status and data1, these should be
  -- alright because of the MIDI routing.
  -- let's just process the value in data2
  
  ------------------------------------------------------------------------------
  
  -- if the bit for the central led is set
  if isBitSet(data2, 6) then
    self.children.led_c.values.x = 1
    data2 = clearBitUnsafe(data2, 6)
  else
    self.children.led_c.values.x = 0
  end
  
  ------------------------------------------------------------------------------
  
  -- get the mode of display
  local mode = 0
  if isBitSet(data2, 5) then
    mode = mode + 2
    data2 = clearBitUnsafe(data2, 5)
  end
  
  if isBitSet(data2, 4) then
    mode = mode + 1
    data2 = clearBitUnsafe(data2, 4)
  end
  
  ------------------------------------------------------------------------------
  
  -- Handle quicker everything turned off
  if data2 == 0 then
    for i = 1, 11, 1 do
      local led = findLed(i)
      led.values.x = 0
    end
    
    return
  end
  
  ------------------------------------------------------------------------------
  
  -- handles more complex modes
  if mode == 0 then
    for i = 1, 11, 1 do
      local led = findLed(i)
      if i == data2 then
        led.values.x = 1
      else
        led.values.x = 0
      end
    end
  elseif mode == 1 then
    for i = 1, 11, 1 do
      local led = findLed(i)
      
      if i <= 6 and data2 <= i then
        led.values.x = 1
      elseif i >= 6 and data2 >= i then
        led.values.x = 1
      else
        led.values.x = 0
      end
    end
  elseif mode == 2 then
    for i = 1, 11, 1 do
      local led = findLed(i)
      if data2 >= i then
        led.values.x = 1
      else
        led.values.x = 0
      end
    end
  else
    local min = 6 - (data2 - 1)
    local max = 6 + (data2 - 1)
    for i = 1, 11, 1 do
      local led = findLed(i)
      
      if i <= 6 and min <= i then
        led.values.x = 1
      elseif i >= 6  and max >= i then
        led.values.x = 1
      else
        led.values.x = 0
      end
    end
  end
end