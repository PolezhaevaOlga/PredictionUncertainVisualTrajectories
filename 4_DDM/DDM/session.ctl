method ks
precision 3.0
set d 0.0
set szr 0.0
set sv 0.0
set st0 0.0
set p 0.0
format subj index_traj path conditions condition cond_sum mean_side mean_val sd last_visibl_side f_missing_pos last_visibl_center_dist[deg] response prop_left TIME exept_prop_left_lv RESPONSE
load "C:/Users/opolezh/Desktop/Paris Saclay/These/4_DATA/data_exp_1/data_clean_v1/cep/cond/*.csv"
save "C:/Users/opolezh/Desktop/Paris Saclay/These/5_MODEL/DDM_exp_1/2_separated_v1/DDM/individual_estimates/*.dat"
