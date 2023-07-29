input metauml;


Component.adapterIn("Adapter")();
Component.proxy("NeMALA::Proxy")();

leftToRight(50)(adapterIn, proxy);

beginfig(1);
	drawObjects(
		adapterIn,
		proxy,
	);
	
	link(requiredInterface)(proxy.ne -- 0.5[adapterIn.ne, proxy.nw]);
	
	link(providedInterface)(adapterIn.ne  -- 0.5[adapterIn.ne, proxy.nw]);
   	link(requiredInterface)(adapterIn.sw + (10,0) -- adapterIn.sw + (10, -20));
	item(iAssoc)("ROS2")(obj.s = adapterIn.s + (0, -30));
	
endfig;

end
