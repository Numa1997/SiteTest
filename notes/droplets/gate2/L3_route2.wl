(* L3 route 2, Wolfram Language 15.0.1 *)
ClearAll[m1, m2, v1, v2, V, dv];
v1v = {a1, a2, a3}; v2v = {b1, b2, b3};
Vv = (m1 v1v + m2 v2v)/(m1 + m2); dvv = v1v - v2v;
Print["(4.1) KE - (M V^2/2 + mu dv^2/2) = ", FullSimplify[m1/2 v1v.v1v + m2/2 v2v.v2v - ((m1 + m2)/2 Vv.Vv + (m1 m2/(m1 + m2))/2 dvv.dvv)]];
Print["v1 - (V + m2/M dv) = ", Simplify[v1v - (Vv + m2/(m1 + m2) dvv)], "   v2 - (V - m1/M dv) = ", Simplify[v2v - (Vv - m1/(m1 + m2) dvv)]];
Print["energy lost in a perfect merger minus CKE = ", FullSimplify[m1/2 v1v.v1v + m2/2 v2v.v2v - (m1 + m2)/2 Vv.Vv - (m1 m2/(m1 + m2))/2 dvv.dvv]];
Print["limit m2->Infinity of mu_red: ", Limit[m1 m2/(m1 + m2), m2 -> Infinity, Assumptions -> m1 > 0]];
Print["merged diameter from volume conservation: ", Solve[Pi/6 dc^3 == Pi/6 (d1^3 + d2^3), dc, Reals]];
ec[We_] := Exp[-115/100 We];
Print["E_coal(0) = ", ec[0], "; limit We->Infinity = ", Limit[ec[We], We -> Infinity], "; derivative = ", D[ec[We], We], "; We for E=1/2: ", N[Solve[ec[We] == 1/2, We][[1, 1, 2]], 6], "; We=0.52 -> E = ", N[ec[52/100], 5], "; We = 61 -> E = ", N[ec[61], 4]];
Print["units of CKE/(Pi sigma d^2): ", UnitSimplify[Quantity[1, "Kilograms" "Meters"^2/"Seconds"^2]/(Quantity[1, "Newtons"/"Meters"] Quantity[1, "Meters"]^2)]];
