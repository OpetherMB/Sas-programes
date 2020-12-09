fvScalarMatrix s43Eqn
(
fvm::ddt(s43)
+ fvm::div(phi, s43)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s43)
==
fvOptions(s43)
);

s43Eqn.relax();
fvOptions.constrain(s43Eqn);
s43Eqn.solve();
fvOptions.correct(s43);
