#### R code: 

up = function(x,y) arrows(x,y+0.33,x,y+0.66,length=0.1,angle=10)
# left arrow
left = function(x,y) arrows(x-0.33,y,x-0.66,y,length=0.1,angle=10)
# diagonal up-left arrow
upleft = function(x,y) arrows(x-0.33,y+0.33,x-0.66,y+0.66,length=0.1,angle=10)

draw_alignment_matrix = function(x)
{
  F = x$F
  ptr = x$Ptr
  
  rows = dim(F)[1]
  cols = dim(F)[2]
  
  plot(0,type="l",lwd=2,axes=FALSE,xlab="",ylab="",
       xlim=c(0,cols+1),ylim=c(0,rows+1))
  
  for (i in 1:rows)
  {
    if (i > 1) up(1,rows-i)
    text(0,rows-i,dimnames(F)[[1]][i])
  }
  for (j in 1:cols)
  {
    if (j > 1) left(j,rows-1)
    text(j,rows,dimnames(F)[[2]][j])
  }
  
  for (i in 1:rows)
  {
    for (j in 1:cols)
    {
      text(j,rows-i,F[i,j])
      if (ptr[i,j] == 2)      { upleft(j,rows-i); }
      else if (ptr[i,j] == 3) { up(j,rows-i); }
      else if (ptr[i,j] == 4) { left(j,rows-i); }
      else if (ptr[i,j] == 5) { upleft(j,rows-i); up(j,rows-i); }
      else if (ptr[i,j] == 6) { upleft(j,rows-i); left(j,rows-i); }
      else if (ptr[i,j] == 7) { up(j,rows-i); left(j,rows-i); }
      else if (ptr[i,j] == 9) { upleft(j,rows-i); up(j,rows-i); left(j,rows-i); }
    }
  }
}


fitting = function(x,y,m,s,d,outfile=NULL) 
{ 
  nx = nchar(x) 
  xx = rep(0,nx) 
  for(i in 1:nx) 
    xx[i] = substr(x,start=i,stop=i) 
  
  ny = nchar(y) 
  yy = rep(0,ny) 
  for(i in 1:ny) 
    yy[i] = substr(y,start=i,stop=i) 
                   
                   # initialize F and ptr 
                   F = ptr = matrix(0,nx+1,ny+1) 
                   dimnames(F) = dimnames(ptr) = list(c("",xx),c("",yy)) 
                   for (i in 1:nx) F[i+1,1] = 0 
                   for (j in 1:ny) F[1,j+1] = -j*d 
                   
                   # main iteration 
                   for (i in 1:nx) 
                   { 
                     for (j in 1:ny) 
                     { 
                       if (xx[i] == yy[j]) 
                       { 
                         t1 = F[i,j] + m 
                       } else  { 
                         t1 = F[i,j] - s
                       } 
                       t2 = F[i,j+1] - d 
                       t3 = F[i+1,j] - d 
                       
                       F[i+1,j+1] = tt = max(t1,t2,t3) 
                       if (t1 == tt) ptr[i+1,j+1] = ptr[i+1,j+1] + 2 
                       if (t2 == tt) ptr[i+1,j+1] = ptr[i+1,j+1] + 3 
                       if (t3 == tt) ptr[i+1,j+1] = ptr[i+1,j+1] + 4 
                     } 
                   } 
                   #if (!is.null(outfile)) print_latex(F,ptr,xx,yy,outfile) 
                   return(list(F = F, Ptr = ptr, outfile=outfile)) 
} 

### run the example 
x = "GTAGGCTTAAGGTTA" 
y = "TAGATA" 
out = fitting (x,y,1,1,1) 
draw_alignment_matrix(out) 
out['F']