###
# #%L
# Tex2Pyomo
# 
# Module name: com.orange.common:tex2pyomo
# Version:     1.0
# Created:     2022-08-24
# %%
# Copyright (C) 2022 Orange
# %%
# The license and distribution terms in 'LGPL-3.0+' for this file may be found 
# in the file 'gnu lesser general public license v3.0 or later - license.txt' in this distribution 
# or LICENSE.txt or at http://www.gnu.org/licenses/lgpl-3.0-standalone.html.
# #L%
###
model.objective = Objective(sense=minimize,rule=lambda model: 0)
model.constraint_summ_4_31 = Constraint(model.TZ,model.S,model.G,rule=lambda model,t,s,g: model.m[t,s,g] == sum([model.m[t,s,g,b] for b in model.B]))
model.constraint_eqincr_4_32 = Constraint(model.T_minus_0,model.S,model.G,model.B,rule=lambda model,t,s,g,b: model.incr[t,s,g,b] >= model.m[t,s,g,b] - model.m[t - 1,s,g,b])
model.constraint_eqdecr_4_33 = Constraint(model.T_minus_0,model.S,model.G,model.B,rule=lambda model,t,s,g,b: model.decr[t,s,g,b] >= model.m[t - 1,s,g,b] - model.m[t,s,g,b])
model.constraint_maxAllocation_4_35 = Constraint(model.S,model.T,model.G,model.B,rule=lambda model,s,t,g,b: model.ω[g] * model.m[t,s,g,b] <= model.ω_[t,g,b])
model.constraint_holdingmax = Constraint(model.T,model.S,model.B,rule=lambda model,t,s,b: sum([model.ω[g] * model.m[t,s,g,b] for g in model.G]) <= model.Ω[t,b])
model.constraint_no_indice_oowqucpw = Constraint(model.T,model.S,model.G,rule=lambda model,t,s,g: sum([model.ω[g_prime] * model.m[t,s,g_prime,model.b] for g_prime in model.G]) <= model.Ω[t,model.b] - model.ω_[t,g,model.b])
model.constraint_idMGmoduleZ_4_38 = Constraint(model.S,model.T,model.G,rule=lambda model,s,t,g: model.m[t,s,g] <= model.M_[g] * model.z[t,s,g])
model.constraint_idAGdecreasingInstall_4_39_forTech_version = Constraint(model.S,model.T,model.G,rule=lambda model,s,t,g: model.z[t - 1,s,g] <= model.z[t,s,g])
model.constraint_isbuilt_new_site_4_68 = Constraint(model.T_minus_0,model.P,model.G,rule=lambda model,t,p,g: model.z[t,p,g] <= model.y[t,p])
model.constraint_idMGinvrule_4_40_all_t_version = Constraint(model.T,model.S,model.G,rule=lambda model,t,s,g: model.m[t,s,g] <= model.M[0,s,g] + (model.M_[g] - model.M[0,s,g]) * model.InvM[g])
model.constraint_idMGinvrule2_4_41_maxi_version = Constraint(model.S,model.G,rule=lambda model,s,g: model.z[model.t_,s,g] <= max(model.Z[0,s,g],model.InvA[g]))
model.constraint_idMGlink_4_42_filteredsum_version = Constraint(model.A,model.T,model.O,rule=lambda model,a,t,o: model.u[t,a,o] == sum([model.u[t,a,o,s,g] for (a,o,s,g) in model.AOSG]))
model.constraint_geoservice_4_45_filtered_forall_version = Constraint(model.AOSG,rule=lambda model,a,o,s,g: model.u[model.t,a,o,s,g] <= model.E[a,s,g] * model.u[model.t,a,o])
model.constraint_GMGcapacite_4_46_filteredsum_version = Constraint(model.S,model.T,model.G,rule=lambda model,s,t,g: sum([model.D[t,o,g] * model.u[t,a,o,s,g] for (a,o,s,g) in model.AOSG]) <= model.CAP[g] * model.m[t,s,g])
model.constraint_GMGuserdynamic_4_47 = Constraint(model.A,model.T,model.O,rule=lambda model,a,t,o: model.u[t,a,o] == model.u[t - 1,a,o] + model.N[t,o] * model.UTOT[t - 1,a] - sum([sum([model.f[σ,c,o] * model.π[t,σ,c,a,o] for c in model.C]) for σ in model.K]))
model.constraint_GMGuserdynamicNO_4_48 = Constraint(model.A,model.T,rule=lambda model,a,t: model.u[t,a,model.NO] == model.u[t - 1,a,model.NO] + model.N[t,model.NO] * model.UTOT[t - 1,a] + sum([sum([sum([model.f[σ,c,o] * model.π[t,σ,c,a,o] for c in model.C]) for σ in model.K]) for o in model.O]))
model.constraint_GMGqoe_4_49_filtered = Constraint(rule=lambda model: sum([model.u[model.t_,a,NO,s,NG] for (a,NO,s,NG) in model.AOSG]) >= model.QoE_ * sum([model.UTOT[model.t_,a] for a in model.A]))
model.constraint_idalphasumz_4_61_corrected_3_13 = Constraint(model.T_minus_0,rule=lambda model,t: model.α[t] * model.N[model.S] == sum([model.z[t,s,model.NG] for s in model.S]))
model.constraint_idMGcov_4_50 = Constraint(rule=lambda model: model.α[model.t_] >= model.α_)
model.constraint_idMGrestriction_oneSubsidy_22_4_51 = Constraint(model.T,model.O,rule=lambda model,t,o: sum([sum([model.δ[t,σ,c,o] for c in model.C]) for σ in model.K]) == 1)
model.constraint_idMGrestriction_var_y_ub2_4_52 = Constraint(model.T,model.C,model.O,rule=lambda model,t,c,o: sum([model.δ[t,σ,c,o] for σ in model.K]) <= 1 + model.U[c] - model.α[t - 1])
model.constraint_idMGrestriction_var_y_lb2_4_53 = Constraint(model.T,model.C,model.O,rule=lambda model,t,c,o: sum([model.δ[t,σ,c,o] for σ in model.K]) <= 1 + model.α[t - 1] - model.L[c])
model.constraint_GMGlin1_4_54 = Constraint(model.A,model.T,model.K,model.C,model.O,rule=lambda model,a,t,σ,c,o: model.π[t,σ,c,a,o] <= model.δ[t,σ,c,o] * model.U_[t - 1,a,o])
model.constraint_GMGlin2_4_55 = Constraint(model.A,model.T,model.K,model.C,model.O,rule=lambda model,a,t,σ,c,o: model.π[t,σ,c,a,o] <= model.u[t - 1,a,o])
model.constraint_GMGlin3_4_56 = Constraint(model.A,model.T,model.K,model.C,model.O,rule=lambda model,a,t,σ,c,o: model.π[t,σ,c,a,o] >= model.u[t - 1,a,o] - (1 - model.δ[t,σ,c,o]) * model.U_[t - 1,a,o])
model.constraint_GMGinit_4_57 = Constraint(model.A,model.O,rule=lambda model,a,o: model.u[0,a,o] == model.U[0,a,o])
model.constraint_idMGLinit_4_58 = Constraint(model.S,model.G,model.B,rule=lambda model,s,g,b: model.m[0,s,g,b] == model.M[0,s,g,b])
model.constraint_idMGinit_4_59 = Constraint(model.S,model.G,rule=lambda model,s,g: model.z[0,s,g] == model.Z[0,s,g])
model.constraint_yy = Constraint(model.P,rule=lambda model,p: model.y[0,p] == 0)
