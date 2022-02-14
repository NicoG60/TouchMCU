function compareTables(t1, t2)
  if #t1 ~= #t2 then return false end

  for i=1,#t1 do
    if t1[i] ~= t2[i] then return false end
  end
  
  return true
end