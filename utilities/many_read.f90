module reader
   use iso_fortran_env, only: int8, int64, int32
   implicit none

contains

   subroutine read_many_files(n_files, bytes_per_file, all_names_len, file_names, buffer)
      integer(int64), intent(in) :: n_files, bytes_per_file, all_names_len
      character(len=*), intent(in) :: file_names
      ! f2py character(f2py_len=all_names_len), depend(all_names_len) :: file_names
      integer(int8), dimension(n_files*bytes_per_file), intent(inout) :: buffer

      integer(int64) :: unit = 12345
      integer(int64) :: i, name_len
      name_len = all_names_len / n_files

      do i=1, n_files
         open(unit,file=trim(file_names((i-1)*name_len+1:i*name_len)), &
         & action="read", access="direct",form="unformatted",status="old",recl=bytes_per_file)
         read(unit,rec=1) buffer( (i-1)*bytes_per_file+1 : i*bytes_per_file )
         close(unit)
      end do

   end subroutine read_many_files

end module reader
