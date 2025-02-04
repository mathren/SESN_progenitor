! ***********************************************************************
!
!   Copyright (C) 2012  Bill Paxton
!
!   this file is part of mesa.
!
!   mesa is free software; you can redistribute it and/or modify
!   it under the terms of the gnu general library public license as published
!   by the free software foundation; either version 2 of the license, or
!   (at your option) any later version.
!
!   mesa is distributed in the hope that it will be useful,
!   but without any warranty; without even the implied warranty of
!   merchantability or fitness for a particular purpose.  see the
!   gnu library general public license for more details.
!
!   you should have received a copy of the gnu library general public license
!   along with this software; if not, write to the free software
!   foundation, inc., 59 temple place, suite 330, boston, ma 02111-1307 usa
!
! ***********************************************************************

module run_star_extras

  use star_lib
  use star_def
  use const_def
  use math_lib
  use chem_def
  use num_lib
  use binary_def
  use ionization_def

  implicit none

  ! these routines are called by the standard run_star check_model
contains


  subroutine extras_controls(id, ierr)
    integer, intent(in) :: id
    integer, intent(out) :: ierr
    type (star_info), pointer :: s
    ierr = 0
    call star_ptr(id, s, ierr)
    if (ierr /= 0) return

    ! this is the place to set any procedure pointers you want to change
    ! e.g., other_wind, other_mixing, other_energy  (see star_data.inc)


    ! the extras functions in this file will not be called
    ! unless you set their function pointers as done below.
    ! otherwise we use a null_ version which does nothing (except warn).

    s% extras_startup => extras_startup
    s% extras_start_step => extras_start_step
    s% extras_check_model => extras_check_model
    s% extras_finish_step => extras_finish_step
    s% extras_after_evolve => extras_after_evolve
    s% how_many_extra_history_columns => how_many_extra_history_columns
    s% data_for_extra_history_columns => data_for_extra_history_columns
    s% how_many_extra_profile_columns => how_many_extra_profile_columns
    s% data_for_extra_profile_columns => data_for_extra_profile_columns

    s% how_many_extra_history_header_items => how_many_extra_history_header_items
    s% data_for_extra_history_header_items => data_for_extra_history_header_items
    s% how_many_extra_profile_header_items => how_many_extra_profile_header_items
    s% data_for_extra_profile_header_items => data_for_extra_profile_header_items

  end subroutine extras_controls


  subroutine extras_startup(id, restart, ierr)
    integer, intent(in) :: id
    logical, intent(in) :: restart
    integer, intent(out) :: ierr
    type (star_info), pointer :: s
    ierr = 0
    call star_ptr(id, s, ierr)
    if (ierr /= 0) return

    s% lxtra(11) = .true. ! do we still need to read inlist_to_CC?

  end subroutine extras_startup


  integer function extras_start_step(id)
    integer, intent(in) :: id
    integer :: ierr
    type (star_info), pointer :: s
    ierr = 0
    call star_ptr(id, s, ierr)
    if (ierr /= 0) return
    extras_start_step = 0

  end function extras_start_step


  ! returns either keep_going, retry, backup, or terminate.
  integer function extras_check_model(id)
    integer, intent(in) :: id
    integer :: ierr
    type (star_info), pointer :: s
    real(dp) :: error, atol, rtol
    ierr = 0
    call star_ptr(id, s, ierr)
    if (ierr /= 0) return
    extras_check_model = keep_going


    ! by default, indicate where (in the code) MESA terminated
    if (extras_check_model == terminate) s% termination_code = t_extras_check_model
  end function extras_check_model


  integer function how_many_extra_history_columns(id)
    integer, intent(in) :: id
    integer :: ierr
    type (star_info), pointer :: s
    ierr = 0
    call star_ptr(id, s, ierr)
    if (ierr /= 0) return
    how_many_extra_history_columns = 0
  end function how_many_extra_history_columns


  subroutine data_for_extra_history_columns(id, n, names, vals, ierr)
    use chem_def, only: chem_isos
    integer, intent(in) :: id, n
    character (len=maxlen_history_column_name) :: names(n)
    real(dp) :: vals(n)
    integer, intent(out) :: ierr
    ! POSYDON output
    real(dp) :: ocz_top_radius, ocz_bot_radius, &
         ocz_top_mass, ocz_bot_mass, mixing_length_at_bcz, &
         dr, ocz_turnover_time_g, ocz_turnover_time_l_b, ocz_turnover_time_l_t, &
         env_binding_E, total_env_binding_E, MoI
    integer :: i, k, n_conv_bdy, nz, k_ocz_bot, k_ocz_top
    integer :: i1, k1, k2, j
    real(dp) :: avg_c_in_c_core
    integer ::  top_bound_zone, bot_bound_zone
    real(dp) :: m_env, Dr_env, Renv_middle, tau_conv, tau_conv_new, m_conv_core, f_conv
    real(dp) :: r_top, r_bottom, m_env_new, Dr_env_new, Renv_middle_new
    !real(dp) :: conv_mx_top, conv_mx_bot, conv_mx_top_r, conv_mx_bot_r, k_div_T_posydon_new, k_div_T_posydon
    !integer :: n_conv_regions_posydon
    integer,  dimension (max_num_mixing_regions) :: n_zones_of_region, bot_bdy, top_bdy
    !real(dp), dimension (max_num_mixing_regions) :: cz_bot_mass_posydon
    !real(dp) :: cz_bot_radius_posydon(max_num_mixing_regions)
    !real(dp), dimension (max_num_mixing_regions) :: cz_top_mass_posydon, cz_top_radius_posydon
    integer :: h1, he4, c12, o16
    real(dp) :: he_core_mass_1cent,  he_core_mass_10cent, he_core_mass_30cent
    real(dp) :: he_core_radius_1cent, he_core_radius_10cent, he_core_radius_30cent
    real(dp) ::  lambda_CE_1cent, lambda_CE_10cent, lambda_CE_30cent, lambda_CE_pure_He_star_10cent
    real(dp),  dimension (:), allocatable ::  adjusted_energy
    real(dp) :: rec_energy_HII_to_HI, &
         rec_energy_HeII_to_HeI, &
         rec_energy_HeIII_to_HeII, &
         diss_energy_H2, &
         frac_HI, frac_HII, &
         frac_HeI, frac_HeII, frac_HeIII, &
         avg_charge_He, energy_comp
    real(dp) :: co_core_mass, co_core_radius
    integer :: co_core_k
    logical :: sticking_to_energy_without_recombination_corr
    real(dp) :: XplusY_CO_core_mass_threshold
    ! to save core-envelope bounday layer
    real(dp) :: offset
    real(dp) :: min_m_boundary, max_m_boundary
    logical :: have_30_value, have_10_value, have_1_value, have_co_value
    ! -------------------------------------
    type (star_info), pointer :: s
    ierr = 0
    call star_ptr(id, s, ierr)
    if (ierr /= 0) return

  end subroutine data_for_extra_history_columns


  integer function how_many_extra_profile_columns(id)
    integer, intent(in) :: id
    integer :: ierr
    type (star_info), pointer :: s
    ierr = 0
    call star_ptr(id, s, ierr)
    if (ierr /= 0) return
    how_many_extra_profile_columns = 0
  end function how_many_extra_profile_columns


  subroutine data_for_extra_profile_columns(id, n, nz, names, vals, ierr)
    integer, intent(in) :: id, n, nz
    character (len=maxlen_profile_column_name) :: names(n)
    real(dp) :: vals(nz,n)
    integer, intent(out) :: ierr
    type (star_info), pointer :: s
    integer :: k
    ierr = 0
    call star_ptr(id, s, ierr)
    if (ierr /= 0) return
  end subroutine data_for_extra_profile_columns


  integer function how_many_extra_history_header_items(id)
    integer, intent(in) :: id
    integer :: ierr
    type (star_info), pointer :: s
    ierr = 0
    call star_ptr(id, s, ierr)
    if (ierr /= 0) return
    how_many_extra_history_header_items = 0
  end function how_many_extra_history_header_items


  subroutine data_for_extra_history_header_items(id, n, names, vals, ierr)
    integer, intent(in) :: id, n
    character (len=maxlen_history_column_name) :: names(n)
    real(dp) :: vals(n)
    type(star_info), pointer :: s
    integer, intent(out) :: ierr
    integer :: i
  end subroutine data_for_extra_history_header_items


  integer function how_many_extra_profile_header_items(id)
    integer, intent(in) :: id
    integer :: ierr
    type (star_info), pointer :: s
    ierr = 0
    call star_ptr(id, s, ierr)
    if (ierr /= 0) return
    how_many_extra_profile_header_items = 0
  end function how_many_extra_profile_header_items


  subroutine data_for_extra_profile_header_items(id, n, names, vals, ierr)
    integer, intent(in) :: id, n
    character (len=maxlen_profile_column_name) :: names(n)
    real(dp) :: vals(n)
    type(star_info), pointer :: s
    integer, intent(out) :: ierr
    ierr = 0
    call star_ptr(id,s,ierr)
    if(ierr/=0) return
  end subroutine data_for_extra_profile_header_items


  ! returns either keep_going or terminate.
  ! note: cannot request retry or backup; extras_check_model can do that.
  integer function extras_finish_step(id)
    integer, intent(in) :: id
    integer :: ierr
    type (star_info), pointer :: s
    ierr = 0
    call star_ptr(id, s, ierr)
    if (ierr /= 0) return
    extras_finish_step = keep_going

    if ((s% center_h1 < 1.0d-2) .and. (s% center_he4 < 1.0d-4) .and. (s% center_c12 < 2.0d-2)) then
       if(s% x_logical_ctrl(1) .and. s% lxtra(11)) then !check for central carbon depletion, only in case we run single stars.
          print *,  "*** Single star depleted carbon ***"
          print *, "read inlist_to_CC"
          call read_star_job(s, "inlist_to_CC", ierr)
          if (ierr /= 0) then
             print *, "Failed reading star_job in inlist_to_CC"
             return
          end if
          print *, "read star_job from inlist_to_CC"
          call star_read_controls(id, "inlist_to_CC", ierr)
          if (ierr /= 0) then
             print *, "Failed reading controls in inlist_to_CC"
             return
          end if
          print *, "read controls from inlist_to_CC"
          s% lxtra(11) = .false. ! avoid re-entering here
       else if (.not. s% x_logical_ctrl(1)) then ! stop
          print *,  "*** Single star depleted carbon ***"
          extras_finish_step = terminate
       end if
    end if

    if (extras_finish_step == terminate) s% termination_code = t_extras_finish_step
  end function extras_finish_step


  subroutine extras_after_evolve(id, ierr)
    integer, intent(in) :: id
    integer, intent(out) :: ierr
    type (star_info), pointer :: s
    ierr = 0
    call star_ptr(id, s, ierr)
    if (ierr /= 0) return
  end subroutine extras_after_evolve
end module run_star_extras
