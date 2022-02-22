
function [Physical_Traj]=localYconvert(extracted_pixel_traj,scanline_idx,homo_matrix)

% input: extracted _traj: n*3 matrix
%        scanline_idx: m*2 matrix
%        homo_matrix: map the scanline_idx to physical coordinates,
%        physical scanline points=homo_matrix:scanline_idx;

x=extracted_pixel_traj(:,1);
ID=extracted_pixel_traj(:,3);

scanline= [scanline_idx,ones(size(scanline_idx,1),1)];    
scanline=scanline.';    
physcanline = homo_matrix*scanline;
Physical_co = physcanline(1:2,:)./[physcanline(3,:);physcanline(3,:)]; 
Physical_co=Physical_co.';

%% convert STmap coordinates to localY
y=[];
for i=1:size(extracted_pixel_traj,1)
    idx=extracted_pixel_traj(i,2);
    y=[y Physical_co(idx,2)];
end
Physical_Traj(:,1)=x;
Physical_Traj(:,2)=y;
Physical_Traj(:,3)=ID;
% display(Physical_Traj);
end


