fvScalarMatrix s79Eqn
(
fvm::ddt(s79)
+ fvm::div(phi, s79)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s79)
==
fvOptions(s79)
);

s79Eqn.relax();
fvOptions.constrain(s79Eqn);
s79Eqn.solve();
fvOptions.correct(s79);
