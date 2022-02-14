function isBitSet(var, bit)
  return var >= 2^bit
end

function setBitUnsafe(var, bit)
  return var + 2^bit
end

function clearBitUnsafe(var, bit)
  return var - 2^bit
end

function setBit(var, bit)
  if isBitSet(var, bit) then
    return var
  else
    return setBitUnsafe(var, bit)
  end
end

function clearBit(var, bit)
  if isBitSet(var, bit) then
    return clearBitUnsafe(var, bit)
  else
    return var
  end
end
