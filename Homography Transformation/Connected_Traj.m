function [Connected_Traj]=Connected_Traj(Detected_traj,Distance_thld)
% This function is used to connect broken trajectories and smooth connected
% trajectories
%  Distance_thld: one parameter can be used to adjust is, which describes
% weather two trajectories are matched


% Detected_traj must have continous IDs

% minimum pixel distance and maxmum pixel distance 
 Trajymin = [];
 Trajymax = [];
% first frame and last frame 
 Trajfmin = [];
 Trajfmax = [];
 
for id = 1 : max(Detected_traj( : , 3))
    Tempt_Traj = Detected_traj(find(Detected_traj( : , 3) == id), : );
    ymin = min(Tempt_Traj( : , 2));
    ymax = max(Tempt_Traj( : , 2));
    Trajymin = [Trajymin ymin];
    Trajymax = [Trajymax ymax];
    fmin = min(Tempt_Traj( : , 1));
    fmax = max(Tempt_Traj( : , 1));
    Trajfmin = [Trajfmin fmin];
    Trajfmax = [Trajfmax fmax];
end

Trajfmin = Trajfmin.';
Trajfmax = Trajfmax.';
Trajymin = Trajymin.';
Trajymax = Trajymax.';
Detected_traj( : , 4) = 0;

% assign same trajectory with same ID

Maps = [];
for id = 1 : max(Detected_traj( : , 3))
    tempt_traj = Detected_traj(find(Detected_traj( : , 3) == id), : );
    group_ids = [];
    group_ids = [group_ids id];    
        mdl0 = fitlm(tempt_traj(1 : min(5, length(tempt_traj)), 1), tempt_traj(1 : min(5, length(tempt_traj)), 2));  
        fmin = tempt_traj(1, 1); fmax = tempt_traj(end, 1);
        ymin = tempt_traj(1, 2); ymax = tempt_traj(end, 2);
        
        % find broken trajectories
        % this line is to find candidates or trajectories for same family
        trajsets_IDs = find( Trajymax < ymin & Trajfmin< fmin & Trajfmax >= max(fmin - 30, 1) & Trajfmax <= (fmin +20));
        
        if ~isempty(trajsets_IDs)
            for j = 1 : size(trajsets_IDs, 1)
                idx = trajsets_IDs(j);
                subtraj = Detected_traj(find(Detected_traj( : , 3) == idx), : );
                
                if subtraj(end,1)<fmin
                    mdl1 = fitlm(subtraj(max(end - 16, 1) : end, 1), subtraj(max(end - 16, 1) : end, 2));
                    ypred1 = predict(mdl1, fmin);
                    ypred0 = predict(mdl0, subtraj(end, 1));
                elseif subtraj(end,1)>= fmin
                    fmin_idx=find(subtraj(:,1)==fmin);
                    mdl1 = fitlm(subtraj(max(fmin_idx - 16, 1) : fmin_idx-1, 1), subtraj(max(fmin_idx - 16, 1) : fmin_idx-1, 2));
                    ypred1 = predict(mdl1, fmin);
                    ypred0 = predict(mdl0, subtraj(end, 1));
                end
                    
%                 abs(ypred1-ymin);
                if abs(ypred1 - ymin) <= Distance_thld & abs(ypred0 - subtraj(end, 2)) <= Distance_thld
                    group_ids = [group_ids idx];
%                 hold on
%                 plot(subtraj(:,1),subtraj(:,2),'r');
%                 hold on
%                 plot(tempt_traj(:,1),tempt_traj(:,2),'r');
                end
            end
        end
        Maps{id} = group_ids;
    end
Maps = Maps.';
% Rearrange trajectory
% Maps contains the connection realtionship between
% different trajectories. we will find all trajectories belong the
% same set

for i = 1 : size(Maps, 1)
    idx_sets = Maps{i};
    for j = 1 : size(Maps)
        compare_sets = Maps{j};
        if ~isempty(intersect(idx_sets, compare_sets))
            idx_sets = unique([idx_sets compare_sets]);
        end 
    end
    Maps{i} = sort(idx_sets);
end

for i = 1 : size(Maps, 1)
    idx_sets = Maps{i};
    Detected_traj(find(Detected_traj( : , 3) == i), 4) = idx_sets(1);
    Maps{i} = idx_sets(1);
end

NewID = findgroups(Detected_traj( : , 4));
Connecting_Traj = Detected_traj( : , 1 : 2);  
Connecting_Traj( : , 3) = NewID;

Clean_Traj = Remove_Zigzag(Connecting_Traj);
Connected_Traj = interpolation(Clean_Traj,20);
